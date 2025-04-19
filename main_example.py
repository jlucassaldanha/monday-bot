import os, time

from voice_reader import pySimpleVoiceRecognition

from simple_twitch_api import AuthorizationCodeGrantFlow
from simple_twitch_api import TwitchClipAPI

auth = AuthorizationCodeGrantFlow()

while True:
    print("::main while")
    while True:
        print("::voice while")
        # Read voice
        rec = pySimpleVoiceRecognition.rec()
        print("::rec")
        # Get response
        result = pySimpleVoiceRecognition.action()
    
        # Break loop
        if result == True:
            msg = "Make a clip"     
            break

    token_file_data = None

    if os.path.exists("credentials.json"):
        auth.read_credentials_file("credentials.json")
        client_id = auth.client_id
        print("Read Credentials")
    else:
        raise Exception("Credentials json file missing")

    if os.path.exists("token.json"):
        token_file_data = auth.read_token_file("token.json")
        print("Read Token")

        if not auth.valid_token:
            print("Refresh Token")
            token_file_data = auth.create_refresh_token(refresh_token=token_file_data['refresh_token'])

    if not token_file_data:
        print("Create Token")
        code = auth.local_server_authorization()
        
        token_file_data = auth.create_refresh_token(code=code)

    token = token_file_data["access_token"]

    api = TwitchClipAPI(client_id, token)

    user_info = api.users_info(['ojoojao'])
    broadcaster_id = user_info[0]["id"]

    api.send_chat_message(broadcaster_id, broadcaster_id, "Criando clipe...")

    created_clip_info = api.create_clip(broadcaster_id)
    clip_id = created_clip_info["id"]

    clip_info = []
    init_time = time.time()
    while len(clip_info) <= 0:
        clip_info = api.get_clip(clip_id)
        
        new_time = time.time()

        if (new_time - init_time) > 15:
            api.send_chat_message(broadcaster_id, broadcaster_id, "Não foi possivel criar o clipe...")
            break

    if (new_time - init_time) < 15:
        api.send_chat_message(broadcaster_id, broadcaster_id, clip_info[0]["url"])