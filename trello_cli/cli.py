import os
import sys
import click
from colorama import init, Fore
import requests

from . import trello_api

# To initialize colorama
init(autoreset=True)

@click.group()
@click.option('--api-key', envvar='TRELLO_API_KEY', help='Trello API key')
@click.option('--token', envvar='TRELLO_TOKEN', help='Trello API token')
@click.pass_context
def cli(ctx, api_key, token):
    """To fetch and store api-key and token in memory"""
    
    # skip API credentials check if the arg is help
    if '--help' in sys.argv or '-h' in sys.argv:
        pass
    else:
        # Check if API credentials are provided
        if not api_key or not token:
            click.echo(f"{Fore.RED}Error: Trello API key and token are required")
            click.echo(f"{Fore.YELLOW}Set TRELLO_API_KEY and TRELLO_TOKEN environment variables or use --api-key and --token options")
            sys.exit(1)
    
    ctx.ensure_object(dict)
    ctx.obj['api_key'] = api_key
    ctx.obj['token'] = token

@cli.command()
@click.option('--board-id', required=True, help='ID of the Trello board')
@click.option('--list-name', required=True, help='Name of the list to add the card to')
@click.option('--title', required=True, help='Card title')
@click.option('--description', default='', help='Card description')
@click.option('--labels', default='', help='Comma-separated list of label colors (e.g., "red,green,blue")')
@click.option('--comment', default='', help='Initial comment on the card')
@click.pass_context
def add_card(ctx, board_id, list_name, title, description, labels, comment):
    """Add a Trello card with labels and a comment to a specified column of a board."""
    api_key = ctx.obj['api_key']
    token = ctx.obj['token']
    
    label_list = [label.strip() for label in labels.split(',')] if labels else []
    
    client = trello_api.TrelloClient(api_key, token)
    
    try:
        # Check if the board Id provided is correct
        client.get_board(board_id)

        # To find the list id for the provided list name
        list_id = client.get_list_id(board_id, list_name)
        if not list_id:
            click.echo(f"{Fore.RED}Error: List '{list_name}' not found on board")
            sys.exit(1)
        
        card = client.add_card(list_id, title, description)
        card_id = card.get('id')
        
        click.echo(f"{Fore.GREEN}Card created successfully: {card.get('shortUrl')}")
        
        # If labels are provided
        if label_list:
            for label in label_list:
                client.add_label(card_id, label)
            click.echo(f"{Fore.BLUE}Added labels: {', '.join(label_list)}")
        
        # If comment are provided
        if comment:
            client.add_comment(card_id, comment)
            click.echo(f"{Fore.BLUE}Added comment to card")
            
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        click.echo(f"{Fore.RED}API Error: {e.response.status_code} - {e.response.text}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)

def main():
    cli(obj={})

if __name__ == '__main__':
    main()