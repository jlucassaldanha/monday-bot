import os, time

from voice_reader import pySimpleVoiceRecognition

from simple_twitch_api import AuthorizationCodeGrantFlow
from simple_twitch_api import TwitchClipAPI

auth = AuthorizationCodeGrantFlow()

while True:
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
    sender_id = "459116718"
    print("Getting user id")

    print("::main while")
    while True:
        print("::voice while")
        # Read voice
        rec = pySimpleVoiceRecognition.rec()
        print("::rec")
        # Criar uma logica para ver se qro fazer um clipe só quando chamar ela
        # Será um metodo que gera um resultado e dependo do resultado ele faz o resto
        # O metodo deve ver se chamei o nome da assistente e somente ele

        # Ver como esta saindo a leitura do lucas para melhorar a chamada
        calling = pySimpleVoiceRecognition.assitent_call()

        if calling:
            api.send_chat_message(broadcaster_id, sender_id, "Oi, me chamou?")

            rec = pySimpleVoiceRecognition.rec()
            print("::rec")
            # Get response
            result = pySimpleVoiceRecognition.action()

            # Logica para se em determinado tempo não sair desse loop, verificar o token novamente
            
            # Break loop
            if result == True:
                msg = "Make a clip"     
                break
            else:
                api.send_chat_message(broadcaster_id, sender_id, "Tá querendo um clipe e não ta sabendo pedir")

    api.send_chat_message(broadcaster_id, sender_id, "Criando clipe...")
    print("Criando clipe...")

    # Talvez botar um delay
    created_clip_info = api.create_clip(broadcaster_id)
    clip_id = created_clip_info["id"]

    clip_info = []
    init_time = time.time()
    while len(clip_info) <= 0:
        clip_info = api.get_clip(clip_id)
        
        new_time = time.time()

        if (new_time - init_time) > 15:
            api.send_chat_message(broadcaster_id, sender_id, "Não foi possivel criar o clipe...")
            print("Não foi possivel criar o clipe...")
            break

    if (new_time - init_time) < 15:
        api.send_chat_message(broadcaster_id, sender_id, clip_info[0]["url"])
        print(clip_info[0]["url"])

    # Danny Jones me descobriu
    # https://www.twitch.tv/dannyjones/clip/CourageousSpookyFriseeTheTarFu-qCyokS5h_4KsNCDq