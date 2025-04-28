import requests, json
from .error_handle import APIRequestsErrors
# Da para melhorar get_clip depois igual o de users, mas são muitos parametros, então vou com calma

###### CRIAR UMA MANEIRA DE VERIFICAR SE O ESCOPO DA FUNÇÂO CHAMADA ESTA NOS ESCOPOS ###########

pasta_atual = __file__
api_dir = "mytwitchapi"

index_main = pasta_atual.find(api_dir) + len(api_dir) # Acha o indice e adiciona mais 3 da palavra procurada
path = pasta_atual[:index_main]

with open(path+"\\error_handle\\errors.json", 'r', encoding="UTF-8") as j_error:
    ERRORS = json.load(j_error)
j_error.close()


class Basics():
    url = ""
    headers = {}
    params = {}
    user_data = {}
    clip_data = {}
    chat_message_data = {}
    created_clip_data = {}

    API_URL_BASE = "https://api.twitch.tv/helix/"
    MESSAGES_URL = "chat/messages" # Não são os scopes
    CHATTERS_URL = "chat/chatters"
    CLIP_URL = "clips"
    USERS_URL = "users"
    FOLLOWS_URL = "streams/followed" 
    MODERATORS_URL = "moderation/moderators" 
    VIPS_URL = "channels/vips"
        
    @classmethod
    def Get_Users(
                    self, 
                    client_id: str, 
                    token: str, 
                    logins: list = None, 
                    ids: list = None
                    ) -> dict:
        
        """
        #### Gets information about one or more users.  
  
        You may look up users using their user ID, login name, or both but the sum total of the number of users you may look up is 100. For example, you may specify 50 IDs and 50 names or 100 IDs or names, but you cannot specify 100 IDs and 100 names.  

        If you don’t specify IDs or login names, the request returns information about the user in the access token if you specify a user access token.  

        To include the user’s verified email address in the response, you must use a user access token that includes the **user:read:email** scope.

        ### Authorization

        Requires an [app access token](https://dev.twitch.tv/docs/authentication/#app-access-tokens) or [user access token](https://dev.twitch.tv/docs/authentication/#user-access-tokens).

        ### URL

        `GET https://api.twitch.tv/helix/users`

        Parameters:
            client_id (str): Client aplication id.

            token (str) : User oauth token.

            ids (list) : The list of ID of the user to get. The maximum number of IDs you may specify is 100.

            logins (list) : The list of login name of the user to get. The maximum number of login names you may specify is 100.

        """
        
        # Verify username parameter are used and construct 
        # the string to append with url of request
        # example: ?login=<username>&login=<username>
        if logins != None:
            if len(logins) <= 100:
                url_data = "?login="+logins[0]

                if len(logins) > 1:
                    for username in logins[1:]:
                        url_data += "&login="+username
            else:
                raise Exception("Number of logins exced the maximum")

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
        if logins != None and ids != None:
            if len(logins) <= 50 and len(ids) <= 50:
                
                url_data = "?login="+logins[0]
                if len(logins) > 1:
                    for username in logins[1:]:
                        url_data += "&login="+username
                
                url_data += "&id="+ids[0]
                if len(ids) > 1:
                    for id in ids[1:]:
                        url_data += "&id="+id
            else:
                raise Exception("Number of logins and ids exced the maximum")

        self.url = self.API_URL_BASE + self.USERS_URL + url_data

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        r = requests.get(url=self.url, headers=self.headers)

        # Return response case of success
        if r.status_code == int(ERRORS['get-users']['errors']['OK CODE']):
            self.user_data = r.json()
            return self.user_data['data']
        
        for k in list(ERRORS['get-users']['errors']):
            if k != ERRORS['get-users']['errors']['OK CODE'] and k != 'OK CODE':

                if r.status_code == int(k):
                    raise APIRequestsErrors(f"{ERRORS['get-users']['errors'][k][0]}:\n{ERRORS['get-users']['errors'][k][1]}")
            
    @classmethod
    def Create_Clip(
                    self, 
                    client_id: str, 
                    token: str, 
                    token_scopes: list,
                    broadcaster_id: str, 
                    has_delay: bool = False
                    ) -> dict:
        """
        #### Creates a clip from the broadcaster’s stream.

        This API captures up to 90 seconds of the broadcaster’s stream. The 90 seconds spans the point in the stream from when you called the API. For example, if you call the API at the 4:00 minute mark, the API captures from approximately the 3:35 mark to approximately the 4:05 minute mark. Twitch tries its best to capture 90 seconds of the stream, but the actual length may be less. This may occur if you begin capturing the clip near the beginning or end of the stream.

        By default, Twitch publishes up to the last 30 seconds of the 90 seconds window and provides a default title for the clip. To specify the title and the portion of the 90 seconds window that’s used for the clip, use the URL in the response’s `edit_url` field. You can specify a clip that’s from 5 seconds to 60 seconds in length. The URL is valid for up to 24 hours or until the clip is published, whichever comes first.

        Creating a clip is an asynchronous process that can take a short amount of time to complete. To determine whether the clip was successfully created, call [Get Clips](#get-clips) using the clip ID that this request returned. If Get Clips returns the clip, the clip was successfully created. If after 15 seconds Get Clips hasn’t returned the clip, assume it failed.

        ### Authorization

        Requires a [user access token](https://dev.twitch.tv/docs/authentication/#user-access-tokens) that includes the **clips:edit** scope.

        ### URL

        `POST https://api.twitch.tv/helix/clips`

        Parameters:
            client_id (str): Client aplication id.

            token (str) : User oauth token.

            broadcaster_id (String) : The ID of the broadcaster whose stream you want to create a clip from.

            has_delay (Boolean) : A Boolean value that determines whether the API captures the clip at the moment the viewer requests it or after a delay. If **false** (default), Twitch captures the clip at the moment the viewer requests it (this is the same clip experience as the Twitch UX). If **true**, Twitch adds a delay before capturing the clip (this basically shifts the capture window to the right slightly).
        """
        needed_scope = "clips:edit"

        self.url = self.API_URL_BASE + self.CLIP_URL

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
        
        # Return response case of success
        if r.status_code == int(ERRORS['create-clip']['errors']['OK CODE']):
            self.user_data = r.json()
            return self.user_data['data']
        
        if not needed_scope in token_scopes:
            raise APIRequestsErrors(f"Error {r.status_code}: Missing needed scope '{needed_scope}'.")
        
        for k in list(ERRORS['create-clip']['errors']):
            if k != ERRORS['create-clip']['errors']['OK CODE'] and k != 'OK CODE':

                if r.status_code == int(k):
                    raise APIRequestsErrors(f"{ERRORS['create-clip']['errors'][k][0]}:\n{ERRORS['create-clip']['errors'][k][1]}")

    @classmethod
    def Get_Clip(
                self, 
                client_id: str, 
                token: str, 
                id: str
                ) -> dict:
        """
        #### Gets one video clip that were captured from streams. For information about clips, see [How to use clips](https://help.twitch.tv/s/article/how-to-use-clips).

        ### Authorization

        Requires an [app access token](https://dev.twitch.tv/docs/authentication/#app-access-tokens) or [user access token](https://dev.twitch.tv/docs/authentication/#user-access-tokens).

        ### URL

        `GET https://api.twitch.tv/helix/clips`

        Parameters:
            client_id (str): Client aplication id.

            token (str) : User oauth token.

            id (String) : An ID that identifies the clip to get. To specify more than one ID, include this parameter for each clip you want to get. For example, `id=foo&id=bar`. You may specify a maximum of 100 IDs. The API ignores duplicate IDs and IDs that aren’t found.

        """
        
        self.url = self.API_URL_BASE + self.CLIP_URL
        # cosntruct params
        self.params = {
            'id' : id
        }

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        r = requests.get(self.url, params=self.params, headers=self.headers)
        
       # Return response case of success
        if r.status_code == int(ERRORS['get-clips']['errors']['OK CODE']):
            self.user_data = r.json()
            return self.user_data['data']
        
        for k in list(ERRORS['get-clips']['errors']):
            if k != ERRORS['get-clips']['errors']['OK CODE'] and k != 'OK CODE':

                if r.status_code == int(k):
                    raise APIRequestsErrors(f"{ERRORS['get-clips']['errors'][k][0]}:\n{ERRORS['get-clips']['errors'][k][1]}")

    @classmethod    
    def Send_Chat_Message(
                            self, 
                            client_id: str, 
                            token: str, 
                            token_scopes: list,
                            broadcaster_id: str, 
                            sender_id: str, 
                            message: str
                            ) -> dict:
        """
        #### NEW Sends a message to the broadcaster’s chat room.

        **NOTE:** When sending messages to a Shared Chat session, behaviors differ depending on your authentication token type:

        * When using an *App Access Token*, messages will only be sent to the source channel (defined by the `broadcaster_id` parameter) by default starting on May 19, 2025. Messages can be sent to all channels by using the `for_source_only` parameter and setting it to `false`.
        * When using a *User Access Token*, messages will be sent to all channels in the shared chat session, including the source channel. This behavior cannot be changed with this token type.

        ### Authorization

        Requires an [app access token](https://dev.twitch.tvhttps://dev.twitch.tv/docs/authentication/#app-access-tokens) or [user access token](https://dev.twitch.tvhttps://dev.twitch.tv/docs/authentication/#user-access-tokens) that includes the `user:write:chat` scope. If app access token used, then additionally requires `user:bot` scope from chatting user, and either `channel:bot` scope from broadcaster or moderator status.

        ### URL

        `POST https://api.twitch.tv/helix/chat/messages`

        Parameters:
            client_id (str): Client aplication id.

            token (str) : User oauth token.

            broadcaster_id (String) : The ID of the broadcaster whose chat room the message will be sent to.

            sender_id (String) : The ID of the user sending the message. This ID must match the user ID in the user access token.

            message (String) : The message to send. The message is limited to a maximum of 500 characters. Chat messages can also include emoticons. To include emoticons, use the name of the emote. The names are case sensitive. Don’t include colons around the name (e.g., :bleedPurple:). If Twitch recognizes the name, Twitch converts the name to the emote before writing the chat message to the chat room

        """
        needed_scope = "user:write:chat"

        self.url = self.API_URL_BASE + self.MESSAGES_URL
        
        # Construct params
        self.params = {
            'broadcaster_id' : broadcaster_id,
            'sender_id' : sender_id,
            'message' : message
        }

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id,
            'Content-Type' : 'application/json'}

        # Make request
        r = requests.post(self.url, params=self.params, headers=self.headers)
        
        # Return response case of success
        if r.status_code == int(ERRORS['send-chat-message']['errors']['OK CODE']):
            self.user_data = r.json()
            return self.user_data['data']
        
        if not needed_scope in token_scopes:
            raise APIRequestsErrors(f"Error {r.status_code}: Missing needed scope '{needed_scope}'.")
        
        for k in list(ERRORS['send-chat-message']['errors']):
            if k != ERRORS['send-chat-message']['errors']['OK CODE'] and k != 'OK CODE':

                if r.status_code == int(k):
                    raise APIRequestsErrors(f"{ERRORS['send-chat-message']['errors'][k][0]}:\n{ERRORS['send-chat-message']['errors'][k][1]}")
        
    @classmethod
    def Get_Followed_Streams(
                            self, 
                            client_id: str, 
                            token: str, 
                            token_scopes: list,
                            user_id: str
                            ) -> dict:
        """
        #### Gets a list of broadcasters that the specified user follows. You can also use this endpoint to see whether a user follows a specific broadcaster.

        ### Authorization

        Requires a [user access token](https://dev.twitch.tv/docs/authentication/#user-access-tokens) that includes the **user:read:follows** scope.

        ### URL

        `GET https://api.twitch.tv/helix/channels/followed`

        Parameters:
            client_id (str): Client aplication id.

            token (str) : User oauth token.

            user_id (String) : A user’s ID. Returns the list of broadcasters that this user follows. This ID must match the user ID in the user OAuth token.

            broadcaster_id (String) : A broadcaster’s ID. Use this parameter to see whether the user follows this broadcaster. If specified, the response contains this broadcaster if the user follows them. If not specified, the response contains all broadcasters that the user follows.

            first (Integer) : The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 100. The default is 20.

            after (String) : The cursor used to get the next page of results. The **Pagination** object in the response contains the cursor’s value. [Read more](https://dev.twitch.tv/docs/api/guide#pagination).
        """
        needed_scope = "user:read:follows"
        
        self.url = self.API_URL_BASE + self.FOLLOWS_URL
        # cosntruct params
        self.params = {
            'user_id' : user_id
        }

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        r = requests.get(self.url, params=self.params, headers=self.headers)
        
        # Return response case of success
        if r.status_code == int(ERRORS['get-followed-streams']['errors']['OK CODE']):
            self.user_data = r.json()
            return self.user_data['data']
        
        if not needed_scope in token_scopes:
            raise APIRequestsErrors(f"Error {r.status_code}: Missing needed scope '{needed_scope}'.")
        
        for k in list(ERRORS['get-followed-streams']['errors']):
            if k != ERRORS['get-followed-streams']['errors']['OK CODE'] and k != 'OK CODE':

                if r.status_code == int(k):
                    raise APIRequestsErrors(f"{ERRORS['get-followed-streams']['errors'][k][0]}:\n{ERRORS['get-followed-streams']['errors'][k][1]}")

    @classmethod  
    def Get_Chatters(
                        self, 
                        client_id: str, 
                        token: str, 
                        token_scopes: list,
                        broadcaster_id: str,
                        moderator_id: str
                        ) -> dict:
        """
        #### Gets the list of users that are connected to the broadcaster’s chat session.

        **NOTE**: There is a delay between when users join and leave a chat and when the list is updated accordingly.

        To determine whether a user is a moderator or VIP, use the [Get Moderators](/docs/api/reference#get-moderators) and [Get VIPs](/docs/api/reference#get-vips) endpoints. You can check the roles of up to 100 users.

        ### Authorization

        Requires a [user access token](https://dev.twitch.tv/docs/authentication/#user-access-tokens) that includes the **moderator:read:chatters** scope.

        ### URL

        `GET https://api.twitch.tv/helix/chat/chatters`

        Parameters:
            client_id (str): Client aplication id.

            token (str) : User oauth token.

            broadcaster_id (String) : The ID of the broadcaster whose list of chatters you want to get.

            moderator_id (String) : The ID of the broadcaster or one of the broadcaster’s moderators. This ID must match the user ID in the user access token.

            first (Integer) : The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 1,000. The default is 100.

            after (String) : The cursor used to get the next page of results. The **Pagination** object in the response contains the cursor’s value. [Read More](/docs/api/guide#pagination)

        """
        needed_scope = "moderator:read:chatters"
        
        self.url = self.API_URL_BASE + self.CHATTERS_URL 
        # cosntruct params
        self.params = {
            'broadcaster_id' : broadcaster_id,
            'moderator_id' : moderator_id
        } # Aprender a usar pagination

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        r = requests.get(self.url, params=self.params, headers=self.headers)
        
        # Return response case of success
        if r.status_code == int(ERRORS['get-chatters']['errors']['OK CODE']):
            self.user_data = r.json()
            return self.user_data['data']
        
        if not needed_scope in token_scopes:
            raise APIRequestsErrors(f"Error {r.status_code}: Missing needed scope '{needed_scope}'.")
        
        for k in list(ERRORS['get-chatters']['errors']):
            if k != ERRORS['get-chatters']['errors']['OK CODE'] and k != 'OK CODE':

                if r.status_code == int(k):
                    raise APIRequestsErrors(f"{ERRORS['get-chatters']['errors'][k][0]}:\n{ERRORS['get-chatters']['errors'][k][1]}")
# melhorar logica do get moderators e vip ######################################################3
    @classmethod  
    def Get_Moderators(
                        self, 
                        client_id: str, 
                        token: str, 
                        token_scopes: list,
                        broadcaster_id: str,
                        user_id: str = None
                        ) -> dict:
        """
        #### Gets all users allowed to moderate the broadcaster’s chat room.

        ### Authorization

        Requires a [user access token](https://dev.twitch.tv/docs/authentication/#user-access-tokens) that includes the **moderation:read** scope. If your app also adds and removes moderators, you can use the **channel:manage:moderators** scope instead.

        ### URL

        `GET https://api.twitch.tv/helix/moderation/moderators`

        Parameters:
            client_id (str): Client aplication id.

            token (str) : User oauth token.

            broadcaster_id (String) : The ID of the broadcaster whose list of moderators you want to get. This ID must match the user ID in the access token.

            user_id (String) : A list of user IDs used to filter the results. To specify more than one ID, include this parameter for each moderator you want to get. For example, `user_id=1234&user_id=5678`. You may specify a maximum of 100 IDs. The returned list includes only the users from the list who are moderators in the broadcaster’s channel. The list is returned in the same order as you specified the IDs.

            first (String) : The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 100 items per page. The default is 20.

            after (String) : The cursor used to get the next page of results. The **Pagination** object in the response contains the cursor’s value. [Read More](/docs/api/guide#pagination)

        """
        needed_scope = "channel:manage:moderators"

        self.url = self.API_URL_BASE + self.MODERATORS_URL

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}
        
        # Caso queira verificar usuarios especificos
        if user_id != None:
            if len(user_id) <= 100:
                ids = "&user_id="+user_id[0]

                if len(user_id) > 1:
                    for id in user_id[1:]:
                        ids += "&user_id="+id
            else:
                raise Exception("Number of ids exced the maximum")

            broadcaster_id = "?broadcaster_id=" + broadcaster_id

            self.url = self.url + broadcaster_id + ids

            r = requests.get(self.url, headers=self.headers)

        # Retorna todos moderadores
        if user_id == None:
            # cosntruct params
            self.params = {
                'broadcaster_id' : broadcaster_id
            } # Aprender a usar pagination

            r = requests.get(self.url, headers=self.headers, params=self.params)       
        
        # Return response case of success
        if r.status_code == int(ERRORS['get-moderators']['errors']['OK CODE']):
            self.user_data = r.json()
            return self.user_data['data']
        
        if not needed_scope in token_scopes:
            raise APIRequestsErrors(f"Error {r.status_code}: Missing needed scope '{needed_scope}'.")

        for k in list(ERRORS['get-moderators']['errors']):
            if k != ERRORS['get-moderators']['errors']['OK CODE'] and k != 'OK CODE':

                if r.status_code == int(k):
                    raise APIRequestsErrors(f"{ERRORS['get-moderators']['errors'][k][0]}:\n{ERRORS['get-moderators']['errors'][k][1]}")
    
    @classmethod  
    def Get_VIPs(
                    self, 
                    client_id: str, 
                    token: str, 
                    token_scopes: list,
                    broadcaster_id: str,
                    user_id: str
                    ) -> dict:
        """
        #### Gets a list of the broadcaster’s VIPs.

        ### Authorization

        Requires a [user access token](https://dev.twitch.tv/docs/authentication/#user-access-tokens) that includes the **channel:read:vips** scope. If your app also adds and removes VIP status, you can use the **channel:manage:vips** scope instead.

        ### URL

        `GET https://api.twitch.tv/helix/channels/vips`

        Parameters:
            client_id (str): Client aplication id.

            token (str) : User oauth token.

            user_id (String) : Filters the list for specific VIPs. To specify more than one user, include the *user\_id* parameter for each user to get. For example, `&user_id=1234&user_id=5678`. The maximum number of IDs that you may specify is 100. Ignores the ID of those users in the list that aren’t VIPs.

            broadcaster_id (String) : The ID of the broadcaster whose list of VIPs you want to get. This ID must match the user ID in the access token.

            first (Integer) : The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 100. The default is 20.

            after (String) : The cursor used to get the next page of results. The **Pagination** object in the response contains the cursor’s value. [Read More](https://dev.twitch.tv/docs/api/guide#pagination)
        """
        needed_scope = "channel:manage:vips"

        self.url = self.API_URL_BASE + self.MODERATORS_URL

        # Create header to requests
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}

        # Caso queira verificar usuarios especificos
        if user_id != None:
            if len(user_id) <= 100:
                ids = "&user_id="+user_id[0]

                if len(user_id) > 1:
                    for id in user_id[1:]:
                        ids += "&user_id="+id
            else:
                raise Exception("Number of ids exced the maximum")

            broadcaster_id = "?broadcaster_id=" + broadcaster_id

            self.url = self.url + broadcaster_id + ids

            r = requests.get(self.url, headers=self.headers)

        # Retorna todos moderadores
        if user_id == None:
            # cosntruct params
            self.params = {
                'broadcaster_id' : broadcaster_id
            } # Aprender a usar pagination

            r = requests.get(self.url, headers=self.headers, params=self.params) 
        
        # Return response case of success
        if r.status_code == int(ERRORS['get-vips']['errors']['OK CODE']):
            self.user_data = r.json()
            return self.user_data['data']
        
        if not needed_scope in token_scopes:
            raise APIRequestsErrors(f"Error {r.status_code}: Missing needed scope '{needed_scope}'.")
        
        for k in list(ERRORS['get-vips']['errors']):
            if k != ERRORS['get-vips']['errors']['OK CODE'] and k != 'OK CODE':

                if r.status_code == int(k):
                    raise APIRequestsErrors(f"{ERRORS['get-vips']['errors'][k][0]}:\n{ERRORS['get-vips']['errors'][k][1]}")
    
# Checklist das funções:
# __init__ - OK
# users_info - OK
# create_clip - OK
# get_clip - OK (melhorar)
# send_chat_message - OK (melhorar)

if __name__ == "__main__":

    #print(ERRORS['get-users']['errors'])

    for k in list(ERRORS['get-users']['errors']):
        if k != ERRORS['get-users']['errors']['OK CODE'] and k != 'OK CODE':
            print("errno:", k)
            print(f"{ERRORS['get-users']['errors'][k][0]}:\n{ERRORS['get-users']['errors'][k][1]}")

