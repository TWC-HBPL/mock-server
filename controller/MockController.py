import json

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from db import SessionLocal
from service.MockService import (
    save_mock_response,
    get_all_mocks,
    get_mock_response,
    update_mock_response, delete_mock_response
)
from models import Log

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def redirect_to_mocks():
    return RedirectResponse(url="/mocks")


@router.get("/mock-ui", response_class=HTMLResponse)
def show_mock_form(request: Request):
    return templates.TemplateResponse("mock_form.html", {"request": request})


@router.post("/mock-ui", response_class=HTMLResponse)
async def handle_mock_form(
        request: Request,
        path: str = Form(...),
        method: str = Form(...),
        response: str = Form(...)
):
    success, msg = save_mock_response(path, method.upper(), response)
    return templates.TemplateResponse("mock_form.html", {
        "request": request,
        "message": msg
    })


@router.get("/mocks", response_class=HTMLResponse)
def show_all_mocks(request: Request):
    mocks = get_all_mocks()

    if not mocks:
        # Save one default mock
        default_path = "/api/v1/default"
        default_method = "GET"
        default_response = json.dumps({"message": "This is a default mock"})
        save_mock_response(default_path, default_method, default_response)

        # Reload after insert
        mocks = get_all_mocks()

    for mock in mocks:
        try:
            mock.response = json.dumps(json.loads(mock.response), indent=2)
        except Exception:
            pass  # Keep raw if invalid

    return templates.TemplateResponse("mock_list.html", {
        "request": request,
        "mocks": mocks
    })


@router.post("/update-mock", response_class=HTMLResponse)
async def update_mock_from_ui(
        request: Request,
        mock_id: int = Form(...),
        path: str = Form(...),
        method: str = Form(...),
        response: str = Form(...)
):
    update_mock_response(mock_id, path, method.upper(), response)
    return RedirectResponse(url="/mocks", status_code=302)


@router.api_route("/mocked/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def serve_mock(path: str, request: Request):
    method = request.method.upper()
    full_path = f"/{path}"
    mock = get_mock_response(full_path, method)

    # Log request
    db = SessionLocal()
    db.add(Log(path=full_path, method=method))
    db.commit()
    db.close()

    if mock:
        try:
            parsed_json = json.loads(mock.response)
            return JSONResponse(content=parsed_json)
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=500,
                content={"error": "Invalid JSON stored for this mock"}
            )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": f"No mock found for {method} {full_path}"}
        )

@router.post("/delete-mock")
def delete_mock(mock_id: int = Form(...)):
    success = delete_mock_response(mock_id)
    return RedirectResponse(url="/mocks", status_code=302)