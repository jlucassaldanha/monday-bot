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
#print(ojoojao_id)

chatters = api.Get_Chatters(ojoojao_id, ojoojao_id)

viewers_ids = [chatter['user_id'] for chatter in chatters]
viewers_users = [chatter['user_name'] for chatter in chatters]
#print(viewers_ids, viewers_users)

mods = api.Get_Moderators(ojoojao_id, viewers_ids)
vips = api.Get_VIPs(ojoojao_id, viewers_ids)

mods_users = [mod['user_name'] for mod in mods]
vips_users = [vip['user_name'] for vip in vips]

viewers_users = list(set(viewers_users) - set(mods_users))
viewers_users = list(set(viewers_users) - set(vips_users))

print(mods_users)
print(vips_users)
print(viewers_users)
