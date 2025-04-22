# Trello CLI

A simple command-line tool to add cards to Trello boards.

## Installation

### Clone the Project
```
git clone git@github.com:prithvi081099/trello-cli.git
cd trello-cli
```

### Create and activate conda environment (optional)
```
conda create -n trello-cli python=3.9
conda activate trello-cli
```

### Install the package
```
pip install -e .
```


## Authentication

You need to provide your Trello API key and token. You can:

### Set them as environment variables:
   ```
   export TRELLO_API_KEY=your_api_key
   export TRELLO_TOKEN=your_token
   ```

### Or pass them directly:
   ```
   trello-cli --api-key YOUR_KEY --token YOUR_TOKEN add-card ...
   ```

### How to Create Trello API Key
1. Log in to your Trello account
2. Visit https://trello.com/power-ups/admin/
3. Click "New" and fill in the details for your API key
4. Once created, you'll receive your API key and can generate a token

## Usage

### Get help
```
trello-cli --help
```

### Add a card to a Trello board
```
trello-cli add-card --board-id BOARD_ID --list-name "To Do" --title "New Card" --description "Test the CLI" --labels "Red,Green" --comment "First comment"
```

#### Parameter Information
- `board-id`: The unique identifier for your Trello board (found in the board URL, e.g., `b6TxDyjL` in `https://trello.com/b/b6TxDyjL/my-board`)
- `list-name`: The name of the list/Column on your board where you want to add the card (e.g., "To Do", "In Progress", "Done")

## Running Tests
To run the test suite:
```
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run a specific test file
pytest tests/test_api.py
```

## Next Development Steps 
1) I'd like to add commands to browse boards and lists so users don't need to look up IDs manually. 
2) I'm planning to implement local caching of Trello data to reduce API calls and make the tool faster. 
3) Looking ahead, I want to add duplicate card detection to prevent accidentally creating the same card twice. 

## Resources Used 
I referenced these docs while working on this project: 
1) Trello API docs for card creation: https://developer.atlassian.com/cloud/trello/rest/api-group-cards/ 
2) Click library for building the CLI: https://click.palletsprojects.com/ 
3) Pytest for writing the tests: https://docs.pytest.org/ 

## Total time taken - 3 hours.