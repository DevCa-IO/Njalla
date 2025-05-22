import pytest
import requests
from unittest.mock import patch, MagicMock
from Njalla.Wallet import NjallaWallet

# Use a dummy API key for mock tests
MOCK_API_KEY = "dummy_api_key_123"
TEST_BASE_URL = "https://njal.la/api/1/"

@pytest.fixture
def njalla_wallet():
    """Fixture to create a Njalla wallet instance"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "balance": 100
            },
            "jsonrpc": "2.0"
        }
        return NjallaWallet(MOCK_API_KEY)

def test_wallet_initialization():
    """Test wallet initialization with valid API key"""
    wallet = NjallaWallet(MOCK_API_KEY)
    assert wallet.api_key == MOCK_API_KEY
    assert wallet.base_url == TEST_BASE_URL
    assert wallet.headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Njalla {MOCK_API_KEY}",
        "Referer": "https://njal.la/",
    }
    assert isinstance(wallet.payment_shorts, dict)
    assert len(wallet.payment_shorts) == 6

def test_add_payment_bitcoin():
    """Test adding payment via Bitcoin"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "amount": 15,
                "amount_btc": "0.0005",
                "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
            },
            "jsonrpc": "2.0"
        }
        wallet = NjallaWallet(MOCK_API_KEY)
        response = wallet.add_payment(amount=15, via="bitcoin")
        assert response["eur_amount"] == 15
        assert response["crypto_amount"] == "0.0005"
        assert response["address"] == "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "add-payment",
                "params": {
                    "amount": 15,
                    "via": "bitcoin"
                }
            },
            headers=wallet.headers
        )

def test_add_payment_paypal():
    """Test adding payment via PayPal"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "amount": 15,
                "url": "https://paypal.com/pay/123"
            },
            "jsonrpc": "2.0"
        }
        wallet = NjallaWallet(MOCK_API_KEY)
        response = wallet.add_payment(amount=15, via="paypal")
        assert response["eur_amount"] == 15
        assert response["url"] == "https://paypal.com/pay/123"

def test_add_payment_invalid_amount():
    """Test adding payment with invalid amount"""
    wallet = NjallaWallet(MOCK_API_KEY)
    with pytest.raises(ValueError, match="Amount must be 5 or multiple of 15, max: 300"):
        wallet.add_payment(amount=4, via="bitcoin")
    with pytest.raises(ValueError, match="Amount must be 5 or multiple of 15, max: 300"):
        wallet.add_payment(amount=301, via="bitcoin")

def test_add_payment_invalid_method():
    """Test adding payment with invalid payment method"""
    wallet = NjallaWallet(MOCK_API_KEY)
    with pytest.raises(ValueError, match="Invalid payment method"):
        wallet.add_payment(amount=15, via="invalid_method")

def test_get_balance():
    """Test getting wallet balance"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "balance": 150
            },
            "jsonrpc": "2.0"
        }
        wallet = NjallaWallet(MOCK_API_KEY)
        balance = wallet.get_balance()
        assert balance == 150
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={"method": "get-balance"},
            headers=wallet.headers
        )

def test_get_payment():
    """Test getting payment details"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "12345",
                "amount": 15,
                "status": "completed",
                "via": "bitcoin"
            },
            "jsonrpc": "2.0"
        }
        wallet = NjallaWallet(MOCK_API_KEY)
        payment = wallet.get_payment(payment_id="12345")
        assert payment["id"] == "12345"
        assert payment["amount"] == 15
        assert payment["status"] == "completed"
        assert payment["via"] == "bitcoin"
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "get-payment",
                "params": {
                    "id": "12345"
                }
            },
            headers=wallet.headers
        )

def test_list_transactions():
    """Test listing transactions"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "transactions": [
                    {
                        "id": "12345",
                        "type": "payment",
                        "amount": 15,
                        "date": "2024-01-01"
                    },
                    {
                        "id": "67890",
                        "type": "registration",
                        "amount": -10,
                        "date": "2024-01-02"
                    }
                ]
            },
            "jsonrpc": "2.0"
        }
        wallet = NjallaWallet(MOCK_API_KEY)
        transactions = wallet.list_transactions()
        assert len(transactions["transactions"]) == 2
        assert transactions["transactions"][0]["type"] == "payment"
        assert transactions["transactions"][1]["type"] == "registration"
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "list-transactions",
                "params": {}
            },
            headers=wallet.headers
        )

def test_error_handling():
    """Test error handling in wallet operations"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "error": {
                "code": 400,
                "message": "Invalid request"
            },
            "jsonrpc": "2.0"
        }
        wallet = NjallaWallet(MOCK_API_KEY)
        with pytest.raises(ValueError, match="Invalid request"):
            wallet.get_balance()

def test_connection_error():
    """Test connection error handling"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.ConnectionError()
        wallet = NjallaWallet(MOCK_API_KEY)
        with pytest.raises(requests.ConnectionError):
            wallet.get_balance()

def test_timeout_error():
    """Test timeout error handling"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.Timeout()
        wallet = NjallaWallet(MOCK_API_KEY)
        with pytest.raises(requests.Timeout):
            wallet.get_balance()

@pytest.mark.real_api
def test_real_api_wallet_operations():
    """Test wallet operations with real API (requires TEST_API_KEY)"""
    import os
    api_key = os.getenv("TEST_API_KEY")
    if not api_key:
        pytest.skip("TEST_API_KEY not set")
    
    wallet = NjallaWallet(api_key)
    
    # Test getting balance
    balance = wallet.get_balance()
    assert isinstance(balance, int)
    
    # Test listing transactions
    transactions = wallet.list_transactions()
    assert "transactions" in transactions
