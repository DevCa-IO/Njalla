import pytest
import requests
from unittest.mock import patch, MagicMock
from Njalla import Client
from Njalla.VPN import NjallaVPN
import os

# Use a dummy API key for mock tests
MOCK_API_KEY = "dummy_api_key_123"
TEST_BASE_URL = "https://njal.la/api/1/"

@pytest.fixture
def mock_response():
    """Fixture to create a mock response object"""
    mock = MagicMock()
    mock.json.return_value = {
        "result": {
            "id": "vpn123",
            "name": "test-vpn",
            "autorenew": True
        },
        "jsonrpc": "2.0"
    }
    return mock

@pytest.fixture
def njalla_vpn():
    """Fixture to create a Njalla VPN instance"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "vpn123",
                "name": "test-vpn",
                "autorenew": True
            },
            "jsonrpc": "2.0"
        }
        return NjallaVPN(MOCK_API_KEY)

def test_vpn_initialization():
    """Test VPN initialization with valid API key"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {"success": True},
            "jsonrpc": "2.0"
        }
        vpn = NjallaVPN(MOCK_API_KEY)
        assert vpn.api_key == MOCK_API_KEY
        assert vpn.base_url == TEST_BASE_URL

def test_vpn_headers():
    """Test VPN headers are correctly set"""
    vpn = NjallaVPN(MOCK_API_KEY)
    expected_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Njalla {MOCK_API_KEY}",
        "Referer": "https://njal.la/",
    }
    assert vpn.headers == expected_headers

def test_add_vpn():
    """Test adding a new VPN client"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "vpn123",
                "name": "test-vpn",
                "autorenew": True
            },
            "jsonrpc": "2.0"
        }
        vpn = NjallaVPN(MOCK_API_KEY)
        response = vpn.add_vpn(
            name="test-vpn",
            autorenew=True
        )
        assert response["id"] == "vpn123"
        assert response["name"] == "test-vpn"
        assert response["autorenew"] is True
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "add-vpn",
                "params": {
                    "name": "test-vpn",
                    "autorenew": True
                }
            },
            headers=vpn.headers
        )

def test_edit_vpn():
    """Test editing an existing VPN client"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "vpn123",
                "name": "updated-vpn",
                "autorenew": False,
                "backend": "wireguard",
                "publickey": "test-key"
            },
            "jsonrpc": "2.0"
        }
        vpn = NjallaVPN(MOCK_API_KEY)
        response = vpn.edit_vpn(
            vpn_id="vpn123",
            name="updated-vpn",
            autorenew=False,
            backend="wireguard",
            publickey="test-key"
        )
        assert response["id"] == "vpn123"
        assert response["name"] == "updated-vpn"
        assert response["autorenew"] is False
        assert response["backend"] == "wireguard"
        assert response["publickey"] == "test-key"

def test_get_vpn():
    """Test getting VPN information"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "vpn123",
                "name": "test-vpn",
                "autorenew": True,
                "backend": "wireguard",
                "publickey": "test-key"
            },
            "jsonrpc": "2.0"
        }
        vpn = NjallaVPN(MOCK_API_KEY)
        response = vpn.get_vpn(vpn_id="vpn123")
        assert response["id"] == "vpn123"
        assert response["name"] == "test-vpn"
        assert response["autorenew"] is True
        assert response["backend"] == "wireguard"
        assert response["publickey"] == "test-key"

def test_list_vpns():
    """Test listing all VPN clients"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "vpns": [
                    {
                        "id": "vpn123",
                        "name": "test-vpn1",
                        "autorenew": True
                    },
                    {
                        "id": "vpn456",
                        "name": "test-vpn2",
                        "autorenew": False
                    }
                ]
            },
            "jsonrpc": "2.0"
        }
        vpn = NjallaVPN(MOCK_API_KEY)
        response = vpn.list_vpns()
        assert len(response) == 2
        assert response[0]["id"] == "vpn123"
        assert response[0]["name"] == "test-vpn1"
        assert response[1]["id"] == "vpn456"
        assert response[1]["name"] == "test-vpn2"

def test_remove_vpn():
    """Test removing a VPN client"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {"success": True},
            "jsonrpc": "2.0"
        }
        vpn = NjallaVPN(MOCK_API_KEY)
        response = vpn.remove_vpn(vpn_id="vpn123")
        assert response["success"] is True
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "remove-vpn",
                "params": {
                    "id": "vpn123"
                }
            },
            headers=vpn.headers
        )

def test_renew_vpn():
    """Test renewing a VPN client"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "vpn123",
                "renewed_until": "2024-12-31"
            },
            "jsonrpc": "2.0"
        }
        vpn = NjallaVPN(MOCK_API_KEY)
        response = vpn.renew_vpn(
            vpn_id="vpn123",
            months=12
        )
        assert response["id"] == "vpn123"
        assert response["renewed_until"] == "2024-12-31"
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "renew-vpn",
                "params": {
                    "id": "vpn123",
                    "months": 12
                }
            },
            headers=vpn.headers
        )

def test_error_handling():
    """Test error handling in VPN operations"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "error": {
                "message": "Invalid VPN ID"
            },
            "jsonrpc": "2.0"
        }
        vpn = NjallaVPN(MOCK_API_KEY)
        with pytest.raises(ValueError) as exc_info:
            vpn.get_vpn(vpn_id="invalid-id")
        assert str(exc_info.value) == "Invalid VPN ID"

def test_connection_error():
    """Test handling of connection errors"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectionError
        vpn = NjallaVPN(MOCK_API_KEY)
        with pytest.raises(requests.exceptions.ConnectionError):
            vpn.list_vpns()

def test_timeout_error():
    """Test handling of timeout errors"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.Timeout
        vpn = NjallaVPN(MOCK_API_KEY)
        with pytest.raises(requests.exceptions.Timeout):
            vpn.list_vpns()

@pytest.mark.real_api
def test_real_api_vpn_operations():
    """Test VPN operations with real API (requires valid API key)"""
    api_key = os.getenv("NJALLA_API_KEY")
    if not api_key:
        pytest.skip("NJALLA_API_KEY environment variable not set")
    
    vpn = NjallaVPN(api_key)
    
    # Test adding a VPN
    add_response = vpn.add_vpn(
        name="test-vpn",
        autorenew=False
    )
    assert "id" in add_response
    
    vpn_id = add_response["id"]
    
    # Test getting VPN info
    get_response = vpn.get_vpn(vpn_id=vpn_id)
    assert get_response["id"] == vpn_id
    
    # Test editing VPN
    edit_response = vpn.edit_vpn(
        vpn_id=vpn_id,
        name="updated-vpn",
        autorenew=True,
        backend="wireguard",
        publickey=None
    )
    assert edit_response["id"] == vpn_id
    
    # Test listing VPNs
    list_response = vpn.list_vpns()
    assert any(v["id"] == vpn_id for v in list_response)
    
    # Test removing VPN
    remove_response = vpn.remove_vpn(vpn_id=vpn_id)
    assert remove_response["success"] is True
