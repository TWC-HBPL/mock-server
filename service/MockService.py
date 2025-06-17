# mockservice.py
from db import SessionLocal
from models import Log, MockResponse
import json



def save_mock_response(path: str, method: str, response: str):
    try:
        parsed_response = json.loads(response)
        json_response = json.dumps(parsed_response)
    except json.JSONDecodeError:
        return False, "Invalid JSON response"

    db = SessionLocal()
    mock = MockResponse(path=path, method=method, response=json_response)
    db.add(mock)
    db.commit()
    db.close()
    return True, f"Mock for {method} {path} saved successfully."


def get_all_mocks():
    db = SessionLocal()
    mocks = db.query(MockResponse).all()
    db.close()
    return mocks


def get_mock_response(path: str, method: str):
    db = SessionLocal()
    mock = db.query(MockResponse).filter_by(path=path, method=method).first()
    db.close()
    return mock


def update_mock_response(mock_id: int, path: str, method: str, response: str):
    try:
        # Validate and re-serialize response to ensure valid JSON
        parsed_response = json.loads(response)
        json_response = json.dumps(parsed_response)  # minified
    except json.JSONDecodeError:
        return False, "Invalid JSON response"

    db = SessionLocal()
    mock = db.query(MockResponse).filter_by(id=mock_id).first()
    if mock:
        mock.path = path
        mock.method = method
        mock.response = json_response
        db.commit()
        db.close()
        return True, "Mock updated."

    db.close()
    return False, "Mock not found."

def delete_mock_response(mock_id: int):
    db = SessionLocal()
    mock = db.query(MockResponse).filter_by(id=mock_id).first()
    if mock:
        db.delete(mock)
        db.commit()
        db.close()
        return True
    db.close()
    return False

