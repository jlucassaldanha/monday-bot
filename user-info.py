from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics

oauth = OAuth()

oauth.credentials("credentials.json")
client_id = oauth.client_id

oauth.access_token("token.json")
token = oauth.token

user_info = Basics.users_info(client_id, token, ['ojoojao'])
print(user_info)

follows = Basics.get_user_follows(client_id, token, user_info[0]["id"])
print(follows)