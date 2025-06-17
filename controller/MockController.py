# mockcontroller.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from service.MockService import get_mock_response, log_request, save_mock_response

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/mock-ui", response_class=HTMLResponse)
async def mock_form(request: Request):
    return templates.TemplateResponse("mock_form.html", {"request": request})

@router.post("/mock-ui", response_class=HTMLResponse)
async def handle_mock_form(
        request: Request,
        path: str = Form(...),
        method: str = Form(...),
        response: str = Form(...)
):
    success, msg = save_mock_response(path, method, response)
    return templates.TemplateResponse("mock_form.html", {
        "request": request,
        "message": msg
    })

@router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, full_path: str):
    method = request.method
    path = "/" + full_path
    response_data = get_mock_response(path, method)
    body_bytes = await request.body()
    body = body_bytes.decode("utf-8") if body_bytes else ""
    log_request(method, path, body, response_data)
    return JSONResponse(content=response_data)