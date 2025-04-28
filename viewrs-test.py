from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics

oauth = OAuth()

oauth.credentials("credentials.json")
client_id = oauth.client_id

oauth.access_token("token.json")
token = oauth.token
scopes = oauth.scopes

api = Basics(client_id, token, scopes)

user_info = api.Get_Users(['ojoojao'])
ojoojao_id = user_info[0]["id"]
print(ojoojao_id)

chatters = api.Get_Chatters(ojoojao_id, ojoojao_id)
print(chatters)

quantidade_viewers = len(chatters)

chatters_ids = []
chatters_usernames = []
for chatter in chatters:
    chatters_ids.append(chatter['user_id'])
    chatters_usernames.append(chatter['user_name'])

mods = api.Get_Moderators(ojoojao_id, chatters_ids)
print(mods)

vips = api.Get_VIPs(ojoojao_id, chatters_ids)
print(vips)

mods_usernames = []
for mod in mods:
    mods_usernames.append(mod['user_name'])
    if mod['user_name'] in chatters_usernames:
        chatters_usernames.remove(mod['user_name'])

vips_usernames = []
for vip in vips:
    vips_usernames.append(vip['user_name'])
    if vip['user_name'] in chatters_usernames:
        chatters_usernames.remove(vip['user_name'])

print("mods:", mods_usernames)
print("vips:", vips_usernames)
print("chatters:", chatters_usernames)