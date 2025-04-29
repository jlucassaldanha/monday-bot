from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics
import time

init = time.time()
oauth = OAuth()

oauth.credentials("credentials.json")
client_id = oauth.client_id

oauth.access_token("token.json")
token = oauth.token
scopes = oauth.scopes

print("oauth:", (time.time() - init))

api = Basics(client_id, token, scopes)

init = time.time()
user_info = api.Get_Users(['ojoojao'])
ojoojao_id = user_info[0]["id"]
#print(ojoojao_id)
print("Get User:", (time.time() - init))

init = time.time()
chatters = api.Get_Chatters(ojoojao_id, ojoojao_id)
print("chatters:", (time.time() - init))

init = time.time()
viewers_ids = [chatter['user_id'] for chatter in chatters]
print("for:", (time.time() - init))
viewers_users = [chatter['user_name'] for chatter in chatters]
#print(viewers_ids, viewers_users)

init = time.time()
mods = api.Get_Moderators(ojoojao_id, viewers_ids)
print("mods:", (time.time() - init))
init = time.time()
vips = api.Get_VIPs(ojoojao_id, viewers_ids)
print("vips:", (time.time() - init))

init = time.time()
mods_users = [mod['user_name'] for mod in mods]
print("mods:", (time.time() - init))
init = time.time()
vips_users = [vip['user_name'] for vip in vips]
print("vips:", (time.time() - init))

init = time.time()
viewers_users = list(set(viewers_users) - set(mods_users))
print("mods:", (time.time() - init))
init = time.time()
viewers_users = list(set(viewers_users) - set(vips_users))
print("vips:", (time.time() - init))

print(mods_users)
print(vips_users)
print(viewers_users)

