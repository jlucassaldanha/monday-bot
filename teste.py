import requests

response = requests.get('https://example.com/nonexistent')
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f'HTTP error occurred: {e}')
else:
    print('Request successful')