from fastapi.testclient import TestClient
from ..main import app
import uuid

client = TestClient(app)


def test_create_customer_and_order():
    unique_email = f"test_{uuid.uuid4().hex}@example.com"

    customer_payload = {
        "name": "Test User",
        "email": unique_email,
        "phone": "1234567890",
        "address": "123 Test St"
    }

    customer_response = client.post("/customers/", json=customer_payload)
    assert customer_response.status_code == 201

    customer_data = customer_response.json()
    assert customer_data["email"] == unique_email
    assert "id" in customer_data

    customer_id = customer_data["id"]

    order_payload = {
        "customer_id": customer_id,
        "description": "Test order",
        "order_status": "pending",
        "order_type": "takeout",
        "promotion_id": None
    }

    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 200

    order_data = order_response.json()
    assert order_data["customer_id"] == customer_id
    assert order_data["description"] == "Test order"
    assert order_data["order_status"] == "pending"
    assert order_data["order_type"] == "takeout"
    assert "tracking_number" in order_data
    assert "id" in order_data
