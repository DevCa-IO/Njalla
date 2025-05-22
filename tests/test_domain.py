import pytest
import requests
from unittest.mock import patch, MagicMock
from Njalla import Client
from Njalla.Domain import NjallaDomain
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
            "domain": "example.com",
            "type": "A",
            "name": "@",
            "content": "1.2.3.4",
            "ttl": 3600
        },
        "jsonrpc": "2.0"
    }
    return mock

@pytest.fixture
def njalla_domain():
    """Fixture to create a Njalla domain instance"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "domain": "example.com",
                "type": "A",
                "name": "@",
                "content": "1.2.3.4",
                "ttl": 3600
            },
            "jsonrpc": "2.0"
        }
        return NjallaDomain(MOCK_API_KEY)

def test_domain_initialization():
    """Test domain initialization with valid API key"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {"success": True},
            "jsonrpc": "2.0"
        }
        domain = NjallaDomain(MOCK_API_KEY)
        assert domain.api_key == MOCK_API_KEY
        assert domain.base_url == TEST_BASE_URL

def test_domain_headers():
    """Test domain headers are correctly set"""
    domain = NjallaDomain(MOCK_API_KEY)
    expected_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Njalla {MOCK_API_KEY}",
        "Referer": "https://njal.la/",
    }
    assert domain.headers == expected_headers

def test_add_dnssec():
    """Test adding DNSSEC record"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {},
            "jsonrpc": "2.0"
        }
        domain = NjallaDomain(MOCK_API_KEY)
        response = domain.add_dnssec(
            domain="example.com",
            algorithm=8,
            digest="1234567890abcdef",
            digest_type=2,
            key_tag=12345
        )
        assert response == {}
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "add-dnssec",
                "params": {
                    "domain": "example.com",
                    "algorithm": 8,
                    "digest": "1234567890abcdef",
                    "digest_type": 2,
                    "key_tag": 12345
                }
            },
            headers=domain.headers
        )

def test_add_forward():
    """Test adding email forward"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "domain": "example.com",
                "from": "test@example.com",
                "to": "forward@example.com"
            },
            "jsonrpc": "2.0"
        }
        domain = NjallaDomain(MOCK_API_KEY)
        response = domain.add_forward(
            domain="example.com",
            from_="test@example.com",
            to="forward@example.com"
        )
        assert response["domain"] == "example.com"
        assert response["from"] == "test@example.com"
        assert response["to"] == "forward@example.com"

def test_add_glue():
    """Test adding glue record"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {},
            "jsonrpc": "2.0"
        }
        domain = NjallaDomain(MOCK_API_KEY)
        response = domain.add_glue(
            domain="example.com",
            name="ns1",
            address4="1.2.3.4",
            address6="2001:db8::1"
        )
        assert response == {}
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "add-glue",
                "params": {
                    "domain": "example.com",
                    "name": "ns1",
                    "address4": "1.2.3.4",
                    "address6": "2001:db8::1"
                }
            },
            headers=domain.headers
        )

def test_add_record():
    """Test adding DNS record"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "id": "12345",
                "domain": "example.com",
                "type": "A",
                "name": "@",
                "content": "1.2.3.4",
                "ttl": 3600
            },
            "jsonrpc": "2.0"
        }
        domain = NjallaDomain(MOCK_API_KEY)
        response = domain.add_record(
            domain="example.com",
            type_="A",
            name="@",
            content="1.2.3.4",
            ttl=3600
        )
        assert response["id"] == "12345"
        assert response["domain"] == "example.com"
        assert response["type"] == "A"
        assert response["name"] == "@"
        assert response["content"] == "1.2.3.4"
        assert response["ttl"] == 3600

def test_edit_domain():
    """Test editing domain configuration"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "name": "example.com",
                "mailforwarding": True,
                "dnssec": True,
                "lock": False
            },
            "jsonrpc": "2.0"
        }
        domain = NjallaDomain(MOCK_API_KEY)
        response = domain.edit_domain(
            domain="example.com",
            mailforwarding=True,
            dnssec=True,
            lock=False
        )
        assert response["name"] == "example.com"
        assert response["mailforwarding"] is True
        assert response["dnssec"] is True
        assert response["lock"] is False

def test_list_records():
    """Test listing DNS records"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "records": [
                    {
                        "id": "12345",
                        "domain": "example.com",
                        "type": "A",
                        "name": "@",
                        "content": "1.2.3.4",
                        "ttl": 3600
                    },
                    {
                        "id": "67890",
                        "domain": "example.com",
                        "type": "MX",
                        "name": "@",
                        "content": "mail.example.com",
                        "ttl": 3600,
                        "prio": 10
                    }
                ]
            },
            "jsonrpc": "2.0"
        }
        domain = NjallaDomain(MOCK_API_KEY)
        response = domain.list_records(domain="example.com")
        assert len(response["records"]) == 2
        assert response["records"][0]["type"] == "A"
        assert response["records"][1]["type"] == "MX"

def test_remove_record():
    """Test removing DNS record"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {},
            "jsonrpc": "2.0"
        }
        domain = NjallaDomain(MOCK_API_KEY)
        response = domain.remove_record(
            domain="example.com",
            id_="12345"
        )
        assert response == {}
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "remove-record",
                "params": {
                    "domain": "example.com",
                    "id": "12345"
                }
            },
            headers=domain.headers
        )

def test_error_handling():
    """Test error handling in domain operations"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "error": {
                "code": 400,
                "message": "Invalid request"
            }
        }
        domain = NjallaDomain(MOCK_API_KEY)
        with pytest.raises(ValueError):
            domain.add_record(
                domain="example.com",
                type_="A",
                name="@",
                content="1.2.3.4"
            )

def test_connection_error():
    """Test connection error handling"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.ConnectionError()
        domain = NjallaDomain(MOCK_API_KEY)
        with pytest.raises(requests.ConnectionError):
            domain.list_records(domain="example.com")

def test_timeout_error():
    """Test timeout error handling"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.Timeout()
        domain = NjallaDomain(MOCK_API_KEY)
        with pytest.raises(requests.Timeout):
            domain.list_records(domain="example.com")

@pytest.mark.real_api
def test_real_api_domain_operations():
    """Test domain operations with real API (requires TEST_API_KEY)"""
    # Try to get the API key from environment
    api_key = os.getenv("TEST_API_KEY")
    if not api_key:
        pytest.skip("TEST_API_KEY not set")
    
    domain = NjallaDomain(api_key)
    
    # Test adding a record
    response = domain.add_record(
        domain="example.com",
        type_="A",
        name="test",
        content="1.2.3.4",
        ttl=3600
    )
    assert "id" in response
    
    # Test listing records
    records = domain.list_records(domain="example.com")
    assert "records" in records
    
    # Test removing the record
    remove_response = domain.remove_record(
        domain="example.com",
        id_=response["id"]
    )
    assert remove_response == {}
