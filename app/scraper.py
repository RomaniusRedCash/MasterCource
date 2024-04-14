import os

import requests
from pprint import pprint
import dotenv

dotenv.load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post(
    'https://stepik.org/oauth2/token/',
    data={'grant_type': 'client_credentials'},
    auth=auth
)

token = response.json().get('access_token', None)

response = requests.get("https://stepik.org/api/courses")

pprint(response.text)