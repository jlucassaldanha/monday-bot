import time

from vosk_transcrib import Transcrib
from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics

oauth = OAuth()
tc = Transcrib()

while True:    

    oauth.credentials("credentials.json")
    client_id = oauth.client_id

    oauth.access_token("token.json")
    token = oauth.token

    user_info = Basics.Get_Users(client_id, token, ['pokimane'])
    broadcaster_id = user_info[0]["id"]
    sender_id = "459116718"
    
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
            Basics.Send_Chat_Message(
                client_id, token, broadcaster_id, sender_id, "Oi, me chamou?"
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
                    Basics.Send_Chat_Message(
                        client_id, token, broadcaster_id, sender_id, 
                        "Tá querendo um clipe e não ta sabendo pedir"
                        )


    Basics.Send_Chat_Message(
        client_id, token, broadcaster_id, sender_id, "Criando clipe..."
        )
    
    print("Criando clipe...")

    # Talvez botar um delay
    created_clip_info = Basics.Create_Clip(client_id, token, broadcaster_id)
    clip_id = created_clip_info["id"]

    clip_info = []
    init_clip_time = time.time()
    while len(clip_info) <= 0:
        clip_info = Basics.Get_Clip(client_id, token, clip_id)
        
        new_clip_time = time.time()

        if (new_clip_time - init_clip_time) > 15:
            Basics.Send_Chat_Message(client_id, token, broadcaster_id, sender_id, 
                                     "Não foi possivel criar o clipe...")
    
            print("Não foi possivel criar o clipe...")
    
            break

    if (new_clip_time - init_clip_time) < 15:
        Basics.Send_Chat_Message(
            client_id, token, broadcaster_id, sender_id, clip_info[0]["url"]
            )
    
        print(clip_info[0]["url"])

    # Danny Jones me descobriu
    # https://www.twitch.tv/dannyjones/clip/CourageousSpookyFriseeTheTarFu-qCyokS5h_4KsNCDq