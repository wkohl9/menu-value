from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_demo_menu_analyzes_every_dish():
    body = client.get("/api/analyze/demo", params={"neighborhood": "Logan Square"}).json()
    assert body["using_sample_data"] is True
    names = [d["item"]["name"] for d in body["dishes"]]
    assert "Wagyu Cheeseburger" in names
    salad = next(d for d in body["dishes"] if d["item"]["name"] == "House Salad")
    assert salad["verdict"] == "not enough data"


def test_text_endpoint():
    resp = client.post(
        "/api/analyze/text",
        json={"text": "Classic Burger 14\nOat Latte 6", "neighborhood": "Pilsen"},
    )
    assert resp.status_code == 200
    assert [d["category"] for d in resp.json()["dishes"]] == ["burger", "latte"]


def test_image_endpoint_says_ocr_not_built_yet():
    resp = client.post(
        "/api/analyze/image",
        files={"image": ("menu.jpg", b"fake-bytes", "image/jpeg")},
    )
    assert resp.status_code == 501


def test_image_endpoint_rejects_non_images():
    resp = client.post(
        "/api/analyze/image",
        files={"image": ("menu.txt", b"hello", "text/plain")},
    )
    assert resp.status_code == 400
