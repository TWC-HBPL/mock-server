# mockservice.py
from db import SessionLocal
from models import Log, MockResponse
import json


def save_mock_response(path, method, response):
    db = SessionLocal()
    try:
        json.loads(response)  # validate JSON
        existing = db.query(MockResponse).filter_by(path=path, method=method.upper()).first()
        if existing:
            existing.response = response
        else:
            mock = MockResponse(path=path, method=method.upper(), response=response)
            db.add(mock)
        db.commit()
        return True, f"Saved mock for {method.upper()} {path}"
    except json.JSONDecodeError:
        return False, "Invalid JSON provided."
    finally:
        db.close()


def get_mock_response(path, method):
    db = SessionLocal()
    try:
        saved = db.query(MockResponse).filter_by(path=path, method=method).first()
        if saved:
            return json.loads(saved.response)
        else:
            return {"message": f"Mock response to {method} {path}"}
    finally:
        db.close()


def log_request(method, path, body, response_data):
    db = SessionLocal()
    try:
        log = Log(method=method, path=path, body=body, response=json.dumps(response_data))
        db.add(log)
        db.commit()
    finally:
        db.close()
