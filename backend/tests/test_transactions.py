"""Tests for all transaction CRUD endpoints and the summary endpoint."""


class TestCreateTransaction:
    def test_create_success(self, client, sample_transaction):
        resp = client.post("/transactions", json=sample_transaction)
        assert resp.status_code == 201
        data = resp.json()
        assert data["description"] == "Test Salary"
        assert data["amount"] == 50000
        assert data["type"] == "income"
        assert data["category"] == "salary"
        assert data["date"] == "2026-03-01"
        assert "id" in data
        assert "created_at" in data

    def test_create_invalid_data(self, client):
        # Missing required fields
        resp = client.post("/transactions", json={"description": "Bad"})
        assert resp.status_code == 422

        # Invalid type
        resp = client.post("/transactions", json={
            "description": "Bad",
            "amount": 100,
            "type": "invalid",
            "category": "food",
            "date": "2026-03-01",
        })
        assert resp.status_code == 422

        # Invalid category
        resp = client.post("/transactions", json={
            "description": "Bad",
            "amount": 100,
            "type": "income",
            "category": "nonexistent",
            "date": "2026-03-01",
        })
        assert resp.status_code == 422

        # Negative amount
        resp = client.post("/transactions", json={
            "description": "Bad",
            "amount": -100,
            "type": "income",
            "category": "salary",
            "date": "2026-03-01",
        })
        assert resp.status_code == 422


class TestListTransactions:
    def test_list_returns_transactions(self, client, sample_transaction, sample_expense):
        client.post("/transactions", json=sample_transaction)
        client.post("/transactions", json=sample_expense)

        resp = client.get("/transactions")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2

    def test_filter_by_type(self, client, sample_transaction, sample_expense):
        client.post("/transactions", json=sample_transaction)
        client.post("/transactions", json=sample_expense)

        resp = client.get("/transactions?type=income")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["type"] == "income"

    def test_search_by_description(self, client, sample_transaction, sample_expense):
        client.post("/transactions", json=sample_transaction)
        client.post("/transactions", json=sample_expense)

        resp = client.get("/transactions?search=Groc")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["description"] == "Groceries"


class TestGetTransaction:
    def test_get_by_id(self, client, sample_transaction):
        create_resp = client.post("/transactions", json=sample_transaction)
        tx_id = create_resp.json()["id"]

        resp = client.get(f"/transactions/{tx_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == tx_id
        assert resp.json()["description"] == "Test Salary"

    def test_get_nonexistent_returns_404(self, client):
        resp = client.get("/transactions/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Transaction not found"


class TestUpdateTransaction:
    def test_update_success(self, client, sample_transaction):
        create_resp = client.post("/transactions", json=sample_transaction)
        tx_id = create_resp.json()["id"]

        updated = {
            "description": "Updated Salary",
            "amount": 60000,
            "type": "income",
            "category": "salary",
            "date": "2026-03-05",
        }
        resp = client.put(f"/transactions/{tx_id}", json=updated)
        assert resp.status_code == 200
        data = resp.json()
        assert data["description"] == "Updated Salary"
        assert data["amount"] == 60000
        assert data["date"] == "2026-03-05"

    def test_update_nonexistent_returns_404(self, client, sample_transaction):
        resp = client.put("/transactions/999", json=sample_transaction)
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Transaction not found"


class TestDeleteTransaction:
    def test_delete_success(self, client, sample_transaction):
        create_resp = client.post("/transactions", json=sample_transaction)
        tx_id = create_resp.json()["id"]

        resp = client.delete(f"/transactions/{tx_id}")
        assert resp.status_code == 204

        # Confirm it's gone
        resp = client.get(f"/transactions/{tx_id}")
        assert resp.status_code == 404

    def test_delete_nonexistent_returns_404(self, client):
        resp = client.delete("/transactions/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Transaction not found"


class TestSummary:
    def test_summary_correct_totals(self, client, sample_transaction, sample_expense):
        client.post("/transactions", json=sample_transaction)
        client.post("/transactions", json=sample_expense)

        resp = client.get("/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_income"] == 50000
        assert data["total_expenses"] == 2500
        assert data["balance"] == 47500

        categories = {c["category"]: c["total"] for c in data["category_breakdown"]}
        assert categories["salary"] == 50000
        assert categories["food"] == 2500

    def test_summary_empty_db(self, client):
        resp = client.get("/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_income"] == 0
        assert data["total_expenses"] == 0
        assert data["balance"] == 0
        assert data["category_breakdown"] == []
