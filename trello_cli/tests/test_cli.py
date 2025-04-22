import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from trello_cli.cli import cli

class TestCli:
    """Test cases for the CLI interface."""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    @patch('trello_cli.trello_api.TrelloClient')
    def test_add_card_success(self, mock_client_class):
        """Test if the card is successfully added."""
        # Set up mock client
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_client.get_board.return_value = {'id': 'board123', 'name': 'Test Board'}
        mock_client.get_list_id.return_value = 'list123'
        mock_client.add_card.return_value = {
            'id': 'card123', 
            'name': 'Test Card',
            'shortUrl': 'https://trello.com/c/card123'
        }
        
        result = self.runner.invoke(
            cli, 
            ['--api-key', 'test_key', '--token', 'test_token', 
             'add-card', '--board-id', 'board123', '--list-name', 'To Do', 
             '--title', 'Test Card', '--description', 'Test Description']
        )
        
        assert result.exit_code == 0
        assert 'Card created successfully' in result.output
        
        mock_client.get_board.assert_called_once_with('board123')
        mock_client.get_list_id.assert_called_once_with('board123', 'To Do')
        mock_client.add_card.assert_called_once()
    
    @patch('trello_cli.trello_api.TrelloClient')
    def test_add_card_with_labels_and_comment(self, mock_client_class):
        """Test adding a labels and a comment to given card_id."""
        # Set up mock client
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_client.get_board.return_value = {'id': 'board123', 'name': 'Test Board'}
        mock_client.get_list_id.return_value = 'list123'
        mock_client.add_card.return_value = {
            'id': 'card123', 
            'name': 'Test Card',
            'shortUrl': 'https://trello.com/c/card123'
        }
        
        result = self.runner.invoke(
            cli, 
            ['--api-key', 'test_key', '--token', 'test_token', 
             'add-card', '--board-id', 'board123', '--list-name', 'To Do', 
             '--title', 'Test Card', '--description', 'Test Description',
             '--labels', 'green,red', '--comment', 'Test Comment']
        )
        
        assert result.exit_code == 0
        assert 'Card created successfully' in result.output
        assert 'Added labels: green, red' in result.output
        assert 'Added comment to card' in result.output
        
        mock_client.add_label.assert_any_call('card123', 'green')
        mock_client.add_label.assert_any_call('card123', 'red')
        mock_client.add_comment.assert_called_once_with('card123', 'Test Comment')
    
    @patch('trello_cli.trello_api.TrelloClient')
    def test_add_card_board_not_found(self, mock_client_class):
        """Test is the provided board_id is incorrect"""
        # Set up mock client
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_client.get_board.side_effect = ValueError("Board with ID 'invalid_id' not found or not accessible.")
        
        result = self.runner.invoke(
            cli, 
            ['--api-key', 'test_key', '--token', 'test_token', 
             'add-card', '--board-id', 'invalid_id', '--list-name', 'To Do', 
             '--title', 'Test Card']
        )
        
        assert result.exit_code == 1
        assert "Board with ID 'invalid_id' not found" in result.output
    
    @patch('trello_cli.trello_api.TrelloClient')
    def test_add_card_list_not_found(self, mock_client_class):
        """Test if the list_name/col_name is incorrect"""
        # Set up mock client
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_client.get_board.return_value = {'id': 'board123', 'name': 'Test Board'}
        mock_client.get_list_id.side_effect = ValueError("List 'Invalid List' not found on the specified board.")
        
        result = self.runner.invoke(
            cli, 
            ['--api-key', 'test_key', '--token', 'test_token', 
             'add-card', '--board-id', 'board123', '--list-name', 'Invalid List', 
             '--title', 'Test Card']
        )
        
        assert result.exit_code == 1
        assert "List 'Invalid List' not found" in result.output