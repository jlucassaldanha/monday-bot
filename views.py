from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics
import time, os


oauth = OAuth()

oauth.credentials("credentials.json")
client_id = oauth.client_id

oauth.access_token("token.json")
token = oauth.token
scopes = oauth.scopes

api = Basics(client_id, token, scopes)

user_info = api.Get_Users(['ojoojao'])
ojoojao_id = user_info[0]["id"]

len_chatters = 0
cred_time = time.time()
while True:
    chatters = api.Get_Chatters(ojoojao_id, ojoojao_id)

    viewers_ids = [chatter['user_id'] for chatter in chatters]
    viewers_users = [chatter['user_name'] for chatter in chatters]

    mods = api.Get_Moderators(ojoojao_id, viewers_ids)
    mods_users = [mod['user_name'] for mod in mods]
    viewers_users = list(set(viewers_users) - set(mods_users))

    len_chatters = len(chatters)

    viewers = [c for c in chatters if c["user_name"] != "ojoojao" and c["user_name"] != "Nightbot" and c["user_name"] != "StreamElements"]

    os.system("cls")
    
    print("\033[0;31;40mEspectadores:\033[m", len(viewers))

    print("Moderadores:")
    for m in mods_users:
        if m != 'Nightbot' and m != 'StreamElements':
            print(f"\033[0;32;40m{m}:\033[m")

    print("Viewers:")
    for v in viewers_users:
        if v != 'ojoojao':
            print(f"\033[0;33;40m{v}:\033[m")


    if (time.time() - cred_time) > 3600:
        oauth.credentials("credentials.json")
        client_id = oauth.client_id

        oauth.access_token("token.json")
        token = oauth.token
        scopes = oauth.scopes

        api = Basics(client_id, token, scopes)

        cred_time = time.time()

    