import pytest
import requests
from unittest.mock import patch, MagicMock
from Njalla import Client
from Njalla.Server import NjallaServer
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
            "id": "server123",
            "name": "Test Server"
        },
        "jsonrpc": "2.0"
    }
    return mock

@pytest.fixture
def njalla_server():
    """Fixture to create a Njalla server instance"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "name": "Test Server"
            },
            "jsonrpc": "2.0"
        }
        return NjallaServer(MOCK_API_KEY)

def test_server_initialization():
    """Test server initialization with valid API key"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {"success": True},
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        assert server.api_key == MOCK_API_KEY
        assert server.base_url == TEST_BASE_URL

def test_server_headers():
    """Test server headers are correctly set"""
    server = NjallaServer(MOCK_API_KEY)
    expected_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Njalla {MOCK_API_KEY}",
        "Referer": "https://njal.la/",
    }
    assert server.headers == expected_headers

def test_add_server():
    """Test adding a new server"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "name": "Test Server",
                "type": "vps",
                "os": "ubuntu-20.04"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.add_server(
            name="Test Server",
            type_="vps",
            os_="ubuntu-20.04",
            ssh_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...",
            months=1,
            autorenew=False
        )
        assert response["id"] == "server123"
        assert response["name"] == "Test Server"
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "add-server",
                "params": {
                    "name": "Test Server",
                    "type": "vps",
                    "os": "ubuntu-20.04",
                    "ssh_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...",
                    "months": 1,
                    "autorenew": False
                }
            },
            headers=server.headers
        )

def test_add_traffic():
    """Test adding extra traffic"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "traffic123",
                "amount": 1000,
                "months": 1
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.add_traffic(
            id_="server123",
            amount=1000,
            months=1,
            starts_today=True
        )
        assert response["id"] == "traffic123"
        assert response["amount"] == 1000
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "add-traffic",
                "params": {
                    "id": "server123",
                    "amount": 1000,
                    "months": 1,
                    "starts_today": True
                }
            },
            headers=server.headers
        )

def test_edit_server():
    """Test editing a server"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "name": "Updated Server",
                "type": "vps",
                "reverse_name": "server.example.com"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.edit_server(
            id_="server123",
            name="Updated Server",
            type_="vps",
            reverse_name="server.example.com",
            autorenew=True
        )
        assert response["id"] == "server123"
        assert response["name"] == "Updated Server"
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "edit-server",
                "params": {
                    "id": "server123",
                    "name": "Updated Server",
                    "type": "vps",
                    "reverse_name": "server.example.com",
                    "autorenew": True
                }
            },
            headers=server.headers
        )

def test_get_server():
    """Test getting server information"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "name": "Test Server",
                "type": "vps",
                "os": "ubuntu-20.04",
                "status": "running"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.get_server(id_="server123")
        assert response["id"] == "server123"
        assert response["name"] == "Test Server"
        assert response["status"] == "running"

def test_list_server_images():
    """Test listing server images"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "images": [
                    {"id": "ubuntu-20.04", "name": "Ubuntu 20.04"},
                    {"id": "debian-11", "name": "Debian 11"}
                ]
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.list_server_images()
        assert len(response) == 2
        assert response[0]["id"] == "ubuntu-20.04"
        assert response[1]["id"] == "debian-11"

def test_list_server_types():
    """Test listing server types"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "types": [
                    {"id": "vps", "name": "VPS"},
                    {"id": "dedicated", "name": "Dedicated"}
                ]
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.list_server_types()
        assert len(response) == 2
        assert response[0]["id"] == "vps"
        assert response[1]["id"] == "dedicated"

def test_list_servers():
    """Test listing servers"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "servers": [
                    {
                        "id": "server123",
                        "name": "Server 1"
                    },
                    {
                        "id": "server456",
                        "name": "Server 2"
                    }
                ]
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.list_servers()
        assert len(response) == 2
        assert response[0]["id"] == "server123"
        assert response[1]["id"] == "server456"

def test_list_traffic():
    """Test listing traffic packages"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "traffic": [
                    {
                        "id": "traffic123",
                        "amount": 1000,
                        "months": 1
                    }
                ]
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.list_traffic(id_="server123")
        assert len(response) == 1
        assert response[0]["id"] == "traffic123"
        assert response[0]["amount"] == 1000

def test_remove_server():
    """Test removing a server"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "task": "task123"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.remove_server(id_="server123")
        assert response["task"] == "task123"

def test_renew_server():
    """Test renewing a server"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "expires": "2024-12-31"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.renew_server(id_="server123", months=12)
        assert response["id"] == "server123"
        assert "expires" in response

def test_reset_server():
    """Test resetting a server"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "status": "resetting"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.reset_server(
            id_="server123",
            os_="ubuntu-20.04",
            ssh_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...",
            type_="vps"
        )
        assert response["id"] == "server123"
        assert response["status"] == "resetting"

def test_restart_server():
    """Test restarting a server"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "status": "restarting"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.restart_server(id_="server123")
        assert response["id"] == "server123"
        assert response["status"] == "restarting"

def test_start_server():
    """Test starting a server"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "status": "starting"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.start_server(id_="server123")
        assert response["id"] == "server123"
        assert response["status"] == "starting"

def test_stop_server():
    """Test stopping a server"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "server123",
                "status": "stopping"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        response = server.stop_server(id_="server123")
        assert response["id"] == "server123"
        assert response["status"] == "stopping"

def test_error_handling():
    """Test error handling in server operations"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "error": {
                "message": "Server not found"
            },
            "jsonrpc": "2.0"
        }
        server = NjallaServer(MOCK_API_KEY)
        with pytest.raises(ValueError) as exc_info:
            server.get_server(id_="invalid-id")
        assert str(exc_info.value) == "Server not found"

def test_connection_error():
    """Test handling of connection errors"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectionError
        server = NjallaServer(MOCK_API_KEY)
        with pytest.raises(requests.exceptions.ConnectionError):
            server.list_servers()

def test_timeout_error():
    """Test handling of timeout errors"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.Timeout
        server = NjallaServer(MOCK_API_KEY)
        with pytest.raises(requests.exceptions.Timeout):
            server.list_servers()

@pytest.mark.real_api
def test_real_api_server_operations():
    """Test server operations with real API (requires valid API key)"""
    api_key = os.getenv("NJALLA_API_KEY")
    if not api_key:
        pytest.skip("NJALLA_API_KEY environment variable not set")
    
    server = NjallaServer(api_key)
    
    # Test listing server types and images
    types = server.list_server_types()
    assert isinstance(types, list)
    
    images = server.list_server_images()
    assert isinstance(images, list)
    
    # Test listing servers
    servers = server.list_servers()
    assert isinstance(servers, list)
    
    if servers:
        # Test getting server info
        server_info = server.get_server(id_=servers[0]["id"])
        assert server_info["id"] == servers[0]["id"]
        
        # Test server operations
        server.restart_server(id_=servers[0]["id"])
        server.stop_server(id_=servers[0]["id"])
        server.start_server(id_=servers[0]["id"])
