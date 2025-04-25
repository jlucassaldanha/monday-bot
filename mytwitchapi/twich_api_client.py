import requests
# Da para melhorar get_clip depois igual o de users, mas são muitos parametros, então vou com calma

class Basics():
    url = ""
    headers = {}
    params = {}
    user_data = {}
    clip_data = {}
    chat_message_data = {}
    created_clip_data = {}

    API_URL_BASE = "https://api.twitch.tv/helix"
    CHAT_URL_SCOPE = "/chat/messages" # Não são os scopes
    CLIP_URL_SCOPE = "/clips"
    USER_URL_SCOPE = "/users"
        
    @classmethod
    def users_info(self, 
                   client_id: str, 
                   token: str, 
                   usernames: list = None, 
                   ids: list = None) -> dict:
        """
        Search for users:
        
        Args:
            client_id (str): Client aplication id.
            token (str): User oauth token.
            usernames (list[(str)] = None: Must be a list of string
                                     with maximum of 100 usernames. 
            ids (list[(str)] = None: Must be a list of string with 
                               maximum of 100 ids.

        In case use both parameters 'usernames' and 'ids', the 
        maximum itens of the list drops to 50 each.

        Returns:
            Users info.
        """
        
        # Verify username parameter are used and construct 
        # the string to append with url of request
        # example: ?login=<username>&login=<username>
        if usernames != None:
            if len(usernames) <= 100:
                url_data = "?login="+usernames[0]

                if len(usernames) > 1:
                    for username in usernames[1:]:
                        url_data += "&login="+username
            else:
                raise Exception("Number of usernames exced the maximum")

        # Same for ids
        if ids != None:
            if len(ids) <= 100:
                url_data = "?id="+ids[0]    
                
                if len(ids) > 1:
                    for id in ids[1:]:
                        url_data += "&id="+id
            else:
                raise Exception("Number of ids exced the maximum")

        # In case of use both parameters, construct one string
        # example: ?login=<username>&login=<username>&id=<id>&id=<id>
        if usernames != None and ids != None:
            if len(usernames) <= 50 and len(ids) <= 50:
                
                url_data = "?login="+usernames[0]
                if len(usernames) > 1:
                    for username in usernames[1:]:
                        url_data += "&login="+username
                
                url_data += "&id="+ids[0]
                if len(ids) > 1:
                    for id in ids[1:]:
                        url_data += "&id="+id
            else:
                raise Exception("Number of usernames and ids exced the maximum")

        self.url = self.API_URL_BASE + self.USER_URL_SCOPE + url_data

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        r = requests.get(url=self.url, headers=self.headers)

        # Return response case of success
        if r.status_code == 200:
            self.user_data = r.json()
            return self.user_data['data']

        # Raise errors codes        
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
    
    @classmethod
    def create_clip(self, 
                    client_id: str, 
                    token: str, 
                    broadcaster_id: str, 
                    has_delay: bool = False) -> dict:
        """
        Create a clip in the broadcaster channel:
        
        Args:
            client_id (str): Client aplication id.
            token (str): User oauth token.
            broadcaster_id (str): Must be id of the broadcaster 
                                  channel wich will be created a clip. 
            has_delay (bool) = False: Creat a clip in the moment 
                               of request in case of False, else, twitch 
                               add a delay betwen request and the creation.

        Returns:
            Createed clip info.
        """
        self.url = self.API_URL_BASE + self.CLIP_URL_SCOPE

        # Construc params
        self.params = {
            'broadcaster_id' : broadcaster_id,
            'has_delay' : has_delay
        }

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        # make the request
        r = requests.post(self.url, params=self.params, headers=self.headers)

        # Return value in case of success
        if r.status_code == 202:
            self.created_clip_data = r.json()
            return self.created_clip_data['data'][0]
        
        # Error codes
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
        if r.status_code == 403:
            raise Exception("HTTPS response error:\n Can't make clips of this broadcaster")
        if r.status_code == 404:
            raise Exception("HTTPS response error:\n Broadcaster must be in live")
    
    @classmethod
    def get_clip(self, 
                 client_id: str, 
                 token: str, 
                 clip_id: str) -> dict:
        """
        Get a clip:
        
        Args:
            client_id (str): Client aplication id.
            token (str): User oauth token.
            clip_id (str): Must be id of the clip. 

        Returns:
            Clip info.
        """
        
        self.url = self.API_URL_BASE + self.CLIP_URL_SCOPE
        # cosntruct params
        self.params = {
            'id' : clip_id
        }

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        r = requests.get(self.url, params=self.params, headers=self.headers)
        
        # Return data in case of success
        if r.status_code == 200:
            self.clip_data = r.json()
            return self.clip_data['data']
        
        # Error codes
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")        
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")

    @classmethod    
    def send_chat_message(self, 
                          client_id: str, 
                          token: str, 
                          broadcaster_id: str, 
                          sender_id: str, 
                          msg: str) -> dict:
        """
        Send a chat message:
        
        Args:
            client_id (str): Client aplication id.
            token (str): User oauth token.
            broadcaster_id (str): Must be id of the broadcaster 
                                  channel wich will be send a chat message. 
            sender_id (str): Must be id of the user wich will be 
                             sending a chat message.
            msg (str): The message chat itself  

        Returns:
            Send message info.
        """
        self.url = self.API_URL_BASE + self.CHAT_URL_SCOPE
        
        # Construct params
        self.params = {
            'broadcaster_id' : broadcaster_id,
            'sender_id' : sender_id,
            'message' : msg
        }

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id,
            'Content-Type' : 'application/json'}

        # Make request
        r = requests.post(self.url, params=self.params, headers=self.headers)
        
        # Return data in case of success
        if r.status_code == 200:
            self.chat_message_data = r.json()
            return self.chat_message_data['data']
                
        # Error codes
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
        if r.status_code == 403:
            raise Exception("HTTPS response error:\n Can't send chat messages to this broadcaster")
        if r.status_code == 422:
            raise Exception("HTTPS response error:\n Message too large to send")
        
    @classmethod
    def get_user_follows(self, 
                 client_id: str, 
                 token: str, 
                 user_id: str) -> dict:
        """
        Get a user followes:
        
        Args:
            client_id (str): Client aplication id.
            token (str): User oauth token.
            user_id (str): Must be id of the user. 

        Returns:
            follow info.
        """
        
        self.url = self.API_URL_BASE + "/streams/followed"
        # cosntruct params
        self.params = {
            'user_id' : user_id
        }

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        r = requests.get(self.url, params=self.params, headers=self.headers)
        
        # Return data in case of success
        if r.status_code == 200:
            self.clip_data = r.json()
            return self.clip_data['data']
        
        # Error codes
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")        
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
    
# Checklist das funções:
# __init__ - OK
# users_info - OK
# create_clip - OK
# get_clip - OK (melhorar)
# send_chat_message - OK (melhorar)


    
        
