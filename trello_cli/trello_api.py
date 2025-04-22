import requests

class TrelloClient:
    """Client for interacting with the Trello API."""
    
    API_URL = "https://api.trello.com/1"
    
    def __init__(self, api_key, token):
        """Initialize the Trello client with API credentials."""
        self.api_key = api_key
        self.token = token
        self.auth_params = {
            'key': api_key,
            'token': token
        }

    def get_board(self, board_id):
        """Check if the provided board_id exists or not """
        url = f"{self.API_URL}/boards/{board_id}"
        try:
            response = requests.get(url, params=self.auth_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Board with ID '{board_id}' not found or not accessible.")
            else:
                raise
    
    def get_list_id(self, board_id, list_name):
        """Find the list_id/Col-name given the list_name"""
        url = f"{self.API_URL}/boards/{board_id}/lists"
        try:
            response = requests.get(url, params=self.auth_params)
            response.raise_for_status()
            
            lists = response.json()
            for lst in lists:
                if lst['name'].lower() == list_name.lower():
                    return lst['id']
            
            # Throw error if the list_name is not found
            raise ValueError(f"List '{list_name}' not found on the specified board.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Board with ID '{board_id}' not found or not accessible.")
            else:
                raise
    
    def add_card(self, list_id, name, desc=""):
        """Add a new card to the specified list and board."""
        url = f"{self.API_URL}/cards"
        data = {
            'idList': list_id,
            'name': name,
            'desc': desc,
            **self.auth_params
        }
        
        response = requests.post(url, params=self.auth_params, data=data)
        response.raise_for_status()
        return response.json()
    
    def add_label(self, card_id, color):
        """Add a label to the specified card_id"""
        url = f"{self.API_URL}/cards/{card_id}/labels"
        data = {
            'color': color.lower(),
            **self.auth_params
        }
        
        response = requests.post(url, params=self.auth_params, data=data)
        response.raise_for_status()
        return response.json()
    
    def add_comment(self, card_id, text):
        """Add a comment to the specified card_id"""
        url = f"{self.API_URL}/cards/{card_id}/actions/comments"
        data = {
            'text': text,
            **self.auth_params
        }
        
        response = requests.post(url, params=self.auth_params, data=data)
        response.raise_for_status()
        return response.json()