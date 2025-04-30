from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics
import time


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

    if len(chatters) != len_chatters:

        viewers_ids = [chatter['user_id'] for chatter in chatters]
        viewers_users = [chatter['user_name'] for chatter in chatters]

        mods = api.Get_Moderators(ojoojao_id, viewers_ids)
        vips = api.Get_VIPs(ojoojao_id, viewers_ids)

        mods_users = [mod['user_name'] for mod in mods]
        vips_users = [vip['user_name'] for vip in vips]

        viewers_users = list(set(viewers_users) - set(mods_users))
        viewers_users = list(set(viewers_users) - set(vips_users))

        len_chatters = len(chatters)

    if (time.time() - cred_time) > 3600:
        oauth.credentials("credentials.json")
        client_id = oauth.client_id

        oauth.access_token("token.json")
        token = oauth.token
        scopes = oauth.scopes

        api = Basics(client_id, token, scopes)

        cred_time = time.time()

    print(mods_users)
    print(vips_users)
    print(viewers_users)

