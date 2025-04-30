from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics

# Criar uma verificação de escopos?

oauth = OAuth()

oauth.credentials("credentials.json")
client_id = oauth.client_id

oauth.access_token("token.json")
token = oauth.token

api = Basics(client_id, token, oauth.scopes)

#user_info = api.Get_Users(['ojoojao'])
#print(user_info)
mod_id = "459116718"
api.Send_Chat_Message(mod_id, mod_id, "teste")

#follows = Basics.Get_Followed_Streams(client_id, token, user_info[0]["id"])
#print(follows)

#clip = Basics.Create_Clip(client_id, token, user_info[0]["id"])
#print(clip)