import time

from vosk_transcrib import Transcrib
from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics

oauth = OAuth()
tc = Transcrib()

init_viewer_time = time.time()
while True:    

    oauth.credentials("credentials.json")
    client_id = oauth.client_id

    oauth.access_token("token.json")
    token = oauth.token
    scopes = oauth.scopes

    api = Basics(client_id, token, scopes)

    user_info = api.Get_Users(['ojoojao'])
    broadcaster_id = user_info[0]["id"]
    sender_id = "459116718"
    ojoojao_id = sender_id

    new_viewers_time = time.time()
    if (new_viewers_time -  init_viewer_time) > 600:
        init_viewer_time = time.time()

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
    
    print("::getting user id")

    print("::main while")
    
    calling = False
    init_voice_time = time.time()
    while True:
        print("::voice while")
    
        # Read voice
        tc.listen_bigbrain()
        pvd = tc.partial
    
        print("::rec")

        #if not calling:
        if (
            "segunda" in pvd["partial"]['list'][1] and
            "feira" in pvd["partial"]['list'][1]
        ):
            print(pvd["partial"]['str'])
            calling = True
            tc.reset()

        new_voice_time = time.time()
        if (new_voice_time - init_voice_time) > 3600:
            oauth.credentials("credentials.json")
            client_id = oauth.client_id

            oauth.access_token("token.json")
            token = oauth.token

        if calling:
            api.Send_Chat_Message(
                broadcaster_id, sender_id, "Oi, me chamou?"
                )

            print("::rec")

            if (
                "faça" in pvd["partial"]['list'][1] or
                "faz" in pvd["partial"]['list'][1]
            ):
                if (
                    "clipe" in pvd["partial"]['list'][1]
                ):
                    print(pvd["partial"]['str'])

                    msg = "Make a clip" 
                    tc.reset()    
                    break

                else:
                    api.Send_Chat_Message(
                        broadcaster_id, sender_id, 
                        "Tá querendo um clipe e não ta sabendo pedir"
                        )


    api.Send_Chat_Message(
        broadcaster_id, sender_id, "Criando clipe..."
        )
    
    print("Criando clipe...")

    # Talvez botar um delay
    created_clip_info = api.Create_Clip(broadcaster_id)
    clip_id = created_clip_info["id"]

    clip_info = []
    init_clip_time = time.time()
    while len(clip_info) <= 0:
        clip_info = api.Get_Clip(clip_id)
        
        new_clip_time = time.time()

        if (new_clip_time - init_clip_time) > 15:
            api.Send_Chat_Message(broadcaster_id, sender_id, 
                                     "Não foi possivel criar o clipe...")
    
            print("Não foi possivel criar o clipe...")
    
            break

    if (new_clip_time - init_clip_time) < 15:
        api.Send_Chat_Message(
            broadcaster_id, sender_id, clip_info[0]["url"]
            )
    
        print(clip_info[0]["url"])

    # Danny Jones me descobriu
    # https://www.twitch.tv/dannyjones/clip/CourageousSpookyFriseeTheTarFu-qCyokS5h_4KsNCDq