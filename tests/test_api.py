import pytest
import requests
from unittest.mock import patch, MagicMock
from Njalla import Client
from Njalla.API import NjallaAPI
import uuid
import os

TEST_API_KEY = os.getenv("TEST_API_KEY")
TEST_BASE_URL = "https://njal.la/api/1/"

@pytest.fixture
def mock_response():
    """Fixture to create a mock response object"""
    mock = MagicMock()
    mock.json.return_value = {
        "result": {
            "comment": "test_comment",
            "created": "2025-05-21T22:41:26Z",
            "key": "8a3cb4afb4147ac13daf3a453dd855e6cf88fa01",
            "from": ["8.8.8.8"],
            "allowed_methods": ["add-record", "edit-record", "remove-record", "list-records"],
            "allowed_types": ["TXT"],
            "allowed_prefixes": ["_acme-challenge"]
        },
        "jsonrpc": "2.0"
    }
    return mock

@pytest.fixture
def njalla_client():
    """Fixture to create a Njalla client instance"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {
                "comment": "test_comment",
                "created": "2025-05-21T22:41:26Z",
                "key": "8a3cb4afb4147ac13daf3a453dd855e6cf88fa01",
                "from": ["8.8.8.8"],
                "allowed_methods": ["add-record", "edit-record", "remove-record", "list-records"],
                "allowed_types": ["TXT"],
                "allowed_prefixes": ["_acme-challenge"]
            },
            "jsonrpc": "2.0"
        }
        return Client(TEST_API_KEY)

def test_client_initialization():
    """Test client initialization with valid API key"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "result": {"success": True},
            "jsonrpc": "2.0"
        }
        client = Client(TEST_API_KEY)
        assert isinstance(client.API, NjallaAPI)
        assert client.API.api_key == TEST_API_KEY
        assert client.API.base_url == TEST_BASE_URL

def test_client_initialization_invalid_key():
    """Test client initialization with invalid API key"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {"error": {"code": 403}}
        with pytest.raises(ValueError, match="Invalid API key"):
            Client(TEST_API_KEY)

def test_api_headers():
    """Test API headers are correctly set"""
    api = NjallaAPI(TEST_API_KEY)
    expected_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Njalla {TEST_API_KEY}",
        "Referer": "https://njal.la/",
    }
    assert api.headers == expected_headers

def test_api_request_timeout():
    """Test API request timeout handling"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.Timeout()
        with pytest.raises(requests.Timeout):
            Client(TEST_API_KEY)

def test_api_request_connection_error():
    """Test API request connection error handling"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.ConnectionError()
        with pytest.raises(requests.ConnectionError):
            Client(TEST_API_KEY)

def test_api_response_error_handling():
    """Test API response error handling"""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "error": {
                "code": 400,
                "message": "Invalid request"
            }
        }
        mock_post.return_value = mock_response
        
        api = NjallaAPI(TEST_API_KEY)
        with pytest.raises(ValueError):
            api.add_token()

def test_api_successful_response():
    """Test successful API response handling"""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": {
                "comment": "test_comment",
                "created": "2025-05-21T22:41:26Z",
                "key": "8a3cb4afb4147ac13daf3a453dd855e6cf88fa01",
                "from": ["8.8.8.8"],
                "allowed_methods": ["add-record", "edit-record", "remove-record", "list-records"],
                "allowed_types": ["TXT"],
                "allowed_prefixes": ["_acme-challenge"]
            },
            "jsonrpc": "2.0"
        }
        mock_post.return_value = mock_response
        
        api = NjallaAPI(TEST_API_KEY)
        response = api.add_token(
            comment="test_comment",
            from_=["8.8.8.8"],
            allowed_methods=["add-record", "edit-record", "remove-record", "list-records"],
            allowed_types=["TXT"],
            allowed_prefixes=["_acme-challenge"],
            acme=True
        )
        assert response["comment"] == "test_comment"
        assert response["key"] == "8a3cb4afb4147ac13daf3a453dd855e6cf88fa01"
        assert response["from"] == ["8.8.8.8"]
        assert response["allowed_methods"] == ["add-record", "edit-record", "remove-record", "list-records"]
        assert response["allowed_types"] == ["TXT"]
        assert response["allowed_prefixes"] == ["_acme-challenge"]

def test_api_method_parameters():
    """Test API method parameter handling"""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": {
                "comment": "test_comment",
                "created": "2025-05-21T22:41:26Z",
                "key": "8a3cb4afb4147ac13daf3a453dd855e6cf88fa01",
                "from": ["8.8.8.8"],
                "allowed_methods": ["add-record", "edit-record", "remove-record", "list-records"],
                "allowed_types": ["TXT"],
                "allowed_prefixes": ["_acme-challenge"]
            },
            "jsonrpc": "2.0"
        }
        mock_post.return_value = mock_response
        
        api = NjallaAPI(TEST_API_KEY)
        
        api.add_token(
            comment="test_comment",
            from_=["8.8.8.8"],
            allowed_methods=["add-record", "edit-record", "remove-record", "list-records"],
            allowed_types=["TXT"],
            allowed_prefixes=["_acme-challenge"],
            acme=True
        )
        
        # Verify the request was made with correct parameters
        mock_post.assert_called_with(
            TEST_BASE_URL,
            json={
                "method": "add-token",
                "params": {
                    "comment": "test_comment",
                    "from": ["8.8.8.8"],
                    "allowed_domains": None,
                    "allowed_servers": None,
                    "allowed_methods": ["add-record", "edit-record", "remove-record", "list-records"],
                    "allowed_prefixes": ["_acme-challenge"],
                    "allowed_types": ["TXT"],
                    "acme": True
                }
            },
            headers=api.headers
        )

def test_mock_edit_token():
    """Test editing a token with mocked response"""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": {
                "comment": "updated_comment",
                "created": "2025-05-21T22:41:26Z",
                "key": "8a3cb4afb4147ac13daf3a453dd855e6cf88fa01",
                "from": ["9.9.9.9"],
                "allowed_methods": ["GET"],
                "allowed_types": ["A"],
                "allowed_prefixes": ["test"]
            },
            "jsonrpc": "2.0"
        }
        mock_post.return_value = mock_response
        
        api = NjallaAPI(TEST_API_KEY)
        response = api.edit_token(
            key="8a3cb4afb4147ac13daf3a453dd855e6cf88fa01",
            comment="updated_comment",
            from_=["9.9.9.9"],
            allowed_methods=["GET"],
            allowed_types=["A"],
            allowed_prefixes=["test"]
        )
        
        assert response["comment"] == "updated_comment"
        assert response["from"] == ["9.9.9.9"]
        assert response["allowed_methods"] == ["GET"]
        assert response["allowed_types"] == ["A"]
        assert response["allowed_prefixes"] == ["test"]

def test_mock_list_tokens():
    """Test listing tokens with mocked response"""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": [
                {
                    "comment": "token1",
                    "created": "2025-05-21T22:41:26Z",
                    "key": "key1",
                    "from": ["8.8.8.8"],
                    "allowed_methods": ["GET"],
                    "allowed_types": ["A"],
                    "allowed_prefixes": ["test"]
                },
                {
                    "comment": "token2",
                    "created": "2025-05-21T22:41:26Z",
                    "key": "key2",
                    "from": ["9.9.9.9"],
                    "allowed_methods": ["POST"],
                    "allowed_types": ["TXT"],
                    "allowed_prefixes": ["_acme"]
                }
            ],
            "jsonrpc": "2.0"
        }
        mock_post.return_value = mock_response
        
        api = NjallaAPI(TEST_API_KEY)
        response = api.list_tokens()
        
        assert len(response) == 2
        assert response[0]["comment"] == "token1"
        assert response[1]["comment"] == "token2"
        assert response[0]["key"] == "key1"
        assert response[1]["key"] == "key2"

def test_mock_remove_token():
    """Test removing a token with mocked response"""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": {"success": True},
            "jsonrpc": "2.0"
        }
        mock_post.return_value = mock_response
        
        api = NjallaAPI(TEST_API_KEY)
        response = api.remove_token("8a3cb4afb4147ac13daf3a453dd855e6cf88fa01")
        
        assert response["success"] is True

@pytest.mark.real_api
def test_real_api_token_lifecycle():
    """
    Test the complete lifecycle of a token:
    1. Create a token
    2. Edit the token
    3. List all tokens
    4. Remove the token
    """
    api = NjallaAPI(TEST_API_KEY)
    uuidString = str(uuid.uuid4())
    token_key = None
    
    try:
        # 1. Create a token
        create_response = api.add_token(
            comment="test_" + uuidString,
            from_=["8.8.8.8"],
            allowed_domains=["example.com"],
            allowed_servers=["server1"],
            allowed_methods=["GET"],
            allowed_prefixes=["test"],
            allowed_types=["A"],
            acme=True
        )
        
        assert "key" in create_response
        assert "created" in create_response
        assert create_response["comment"] == "test_" + uuidString
        assert create_response["from"] == ["8.8.8.8"]
        assert create_response["allowed_methods"] == ["add-record", "edit-record", "remove-record", "list-records"]
        assert create_response["allowed_types"] == ["TXT"]
        assert create_response["allowed_prefixes"] == ["_acme-challenge"]
        
        token_key = create_response["key"]
        
        # 2. Edit the token - only edit comment and from_ fields for ACME tokens
        edit_response = api.edit_token(
            key=token_key,
            comment="updated_" + uuidString,
            from_=["9.9.9.9"]
        )
        
        assert edit_response["comment"] == "updated_" + uuidString
        assert edit_response["from"] == ["9.9.9.9"]
        assert edit_response["allowed_methods"] == ["add-record", "edit-record", "remove-record", "list-records"]
        assert edit_response["allowed_types"] == ["TXT"]
        assert edit_response["allowed_prefixes"] == ["_acme-challenge"]
        
        # 3. List all tokens
        list_response = api.list_tokens()
        assert isinstance(list_response, list)
        found_token = False
        for token in list_response:
            if token["key"] == token_key:
                found_token = True
                assert token["comment"] == "updated_" + uuidString
                assert token["from"] == ["9.9.9.9"]
                break
        assert found_token, "Created token not found in list"
        
        # 4. Remove the token
        remove_response = api.remove_token(token_key)
        assert remove_response["success"] is True
        
        # Verify token is removed
        list_response = api.list_tokens()
        for token in list_response:
            assert token["key"] != token_key, "Token was not properly removed"
            
    except ValueError as e:
        pytest.fail(f"API call failed with error: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")
