
# Import module
from tkinter import *
import datetime

from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics
import time, os


def creds():
    global client_id, token, scopes

    oauth = OAuth()

    oauth.credentials("credentials.json")
    client_id = oauth.client_id

    oauth.access_token("token.json")
    token = oauth.token
    scopes = oauth.scopes

    root.after(3600000, creds)


def get_viewers():
    global viewers_count, viewers_txt, mods_txt
    ojoojao_id = "459116718"
    
    api = Basics(client_id, token, scopes)

    
    chatters = api.Get_Chatters(ojoojao_id, ojoojao_id)

    viewers_ids = [chatter['user_id'] for chatter in chatters]
    viewers_users = [chatter['user_name'] for chatter in chatters]

    mods = api.Get_Moderators(ojoojao_id, viewers_ids)
    mods_users = [mod['user_name'] for mod in mods]
    viewers_users = list(set(viewers_users) - set(mods_users))

    viewers = [c for c in chatters if c["user_name"] != "ojoojao" and c["user_name"] != "Nightbot" and c["user_name"] != "StreamElements"]

    mods_txt = ""
    for m in mods_users:
        if m != 'Nightbot' and m != 'StreamElements':
            mods_txt += m + "\n"

    viewers_txt = ""
    for v in viewers_users:
        if v != 'ojoojao':
            viewers_txt += v + "\n"

    viewers_count = str(len(viewers))

    return mods_txt, viewers_txt, viewers_count  

def update_values():
    get_viewers()
    v_count['text'] = "Espectadores: " + viewers_count
    v['text'] = "Espectadores:\n" + viewers_txt
    m['text'] ="Moderadores:\n" + mods_txt
    root.after(60000, update_values)
 
# Create object
root = Tk()
 
root.wm_attributes('-transparentcolor', root['bg'])
root.attributes("-topmost", True)

v_count = Label(root, text="placeholder", fg="red", font=("helvetica", 15))
v_count.grid(row=0, column=0)
v = Label(root, text="placeholder", fg="green", font=("helvetica", 15))
v.grid(row=1, column=0)
m = Label(root, text="placeholder", fg="yellow", font=("helvetica", 15))
m.grid(row=2, column=0)

creds() 
update_values()

# Execute tkinter
root.mainloop()