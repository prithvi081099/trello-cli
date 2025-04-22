import pytest
import requests
from unittest.mock import patch, MagicMock
from trello_cli.trello_api import TrelloClient

class TestTrelloClient:
    """Test cases for the TrelloClient class."""
    
    def setup_method(self):
        self.client = TrelloClient('test_api_key', 'test_token')
    
    @patch('requests.get')
    def test_get_board_success(self, mock_get):
        """Test when board_id is correct"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {'id': 'board123', 'name': 'Test Board'}
        mock_get.return_value = mock_response
        
        result = self.client.get_board('board123')
        
        assert result['id'] == 'board123'
        assert result['name'] == 'Test Board'
        mock_get.assert_called_once_with(
            'https://api.trello.com/1/boards/board123', 
            params={'key': 'test_api_key', 'token': 'test_token'}
        )
    
    @patch('requests.get')
    def test_get_board_not_found(self, mock_get):
        """Test if the board_id is incorrect"""

        mock_response = MagicMock()
        http_error = requests.exceptions.HTTPError()
        
        mock_error_response = MagicMock()
        mock_error_response.status_code = 404
        http_error.response = mock_error_response
        
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Board with ID 'invalid_id' not found or not accessible."):
            self.client.get_board('invalid_id')
    
    @patch('requests.get')
    def test_get_list_id_success(self, mock_get):
        """Test getting the list_id when the correct list_name is provided"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'id': 'list123', 'name': 'To Do'},
            {'id': 'list456', 'name': 'Doing'}
        ]
        mock_get.return_value = mock_response
        
        result = self.client.get_list_id('board123', 'To Do')
        
        assert result == 'list123'
        mock_get.assert_called_once_with(
            'https://api.trello.com/1/boards/board123/lists', 
            params={'key': 'test_api_key', 'token': 'test_token'}
        )
    
    @patch('requests.get')
    def test_get_list_id_not_found(self, mock_get):
        """Test when incorrect list_name is provided"""

        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'id': 'list123', 'name': 'To Do'},
            {'id': 'list456', 'name': 'Doing'}
        ]
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="List 'Not Exists' not found on the specified board."):
            self.client.get_list_id('board123', 'Not Exists')
    
    @patch('requests.post')
    def test_add_card_success(self, mock_post):
        """Test adding a card successfully."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 'card123', 
            'name': 'Test Card',
            'shortUrl': 'https://trello.com/c/card123'
        }
        mock_post.return_value = mock_response
        
        result = self.client.add_card('list123', 'Test Card', 'Test Description')
        
        assert result['id'] == 'card123'
        assert result['name'] == 'Test Card'
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_add_label_success(self, mock_post):
        """Test adding a label successfully."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {'id': 'label123', 'color': 'green'}
        mock_post.return_value = mock_response
        
        result = self.client.add_label('card123', 'green')
        
        assert result['id'] == 'label123'
        assert result['color'] == 'green'
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_add_comment_success(self, mock_post):
        """Test adding a comment successfully."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {'id': 'comment123', 'text': 'Test Comment'}
        mock_post.return_value = mock_response
        
        result = self.client.add_comment('card123', 'Test Comment')
        
        assert result['id'] == 'comment123'
        assert result['text'] == 'Test Comment'
        mock_post.assert_called_once()