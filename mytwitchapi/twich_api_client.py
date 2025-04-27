import requests, json
from exceptions import APIRequestsErrors
# Da para melhorar get_clip depois igual o de users, mas são muitos parametros, então vou com calma

pasta_atual = __file__
api_dir = "mytwitchapi"

index_main = pasta_atual.find(api_dir) + len(api_dir) # Acha o indice e adiciona mais 3 da palavra procurada
path = pasta_atual[:index_main]

with open(path+"\\errors.json", 'r', encoding="UTF-8") as j_error:
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
        if r.status_code == 200:
            self.user_data = r.json()
            return self.user_data['data']

        # Raise errors codes        
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
    
    @classmethod
    def Create_Clip(self, 
                    client_id: str, 
                    token: str, 
                    broadcaster_id: str, 
                    has_delay: bool = False) -> dict:
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
    def Get_Clip(self, 
                 client_id: str, 
                 token: str, 
                 id: str) -> dict:
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
    def Send_Chat_Message(self, 
                          client_id: str, 
                          token: str, 
                          broadcaster_id: str, 
                          sender_id: str, 
                          message: str) -> dict:
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
    def Get_Followed_Streams(self, 
                 client_id: str, 
                 token: str, 
                 user_id: str) -> dict:
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
    def Get_Chatters(self, 
                     client_id: str, 
                     token: str, 
                     broadcaster_id: str,
                     moderator_id: str) -> dict:
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
        
        # Return data in case of success
        if r.status_code == 200:
            self.clip_data = r.json()
            return self.clip_data['data']
        
        # Error codes
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")        
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
        if r.status_code == 403:
            raise Exception("HTTPS response error:\n Not a moderator of thos channel")
        
    @classmethod  
    def Get_Moderatos(self, 
                     client_id: str, 
                     token: str, 
                     broadcaster_id: str,
                     user_id: str) -> dict:
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
        
        self.url = self.API_URL_BASE + self.MODERATORS_URL
        # cosntruct params
        self.params = {
            'broadcaster_id' : broadcaster_id,
            'user_id' : user_id
        } # Aprender a usar pagination

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
    def Get_VIPs(self, 
                     client_id: str, 
                     token: str, 
                     broadcaster_id: str,
                     user_id: str) -> dict:
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
        
        self.url = self.API_URL_BASE + "channels/vips"
        # cosntruct params
        self.params = {
            'broadcaster_id' : broadcaster_id,
            'user_id' : user_id
        } # Aprender a usar pagination

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

if __name__ == "__main__":

    with open(path+"\\infos.json", 'r', encoding="UTF-8") as j_info:
        INFOS = json.load(j_info)
    j_info.close()

    for func in INFOS.keys():
        function_info = INFOS[func]

        title = "\n\n" + func + "\n\n"

        info = "#### " + function_info['info'] + "\n\nParameters:\n"
        
        if info.find("/docs/authentication#app-access-tokens") != -1:
            info = str(info).replace("/docs/authentication#app-access-tokens", "https://dev.twitch.tv/docs/authentication/#app-access-tokens")

        if info.find("/docs/authentication#user-access-tokens") != -1:
            info = str(info).replace("/docs/authentication#user-access-tokens", "https://dev.twitch.tv/docs/authentication/#user-access-tokens")

        query_params = function_info['query']
        query = ""
        if not "None" in query_params.keys():
            for k in query_params.keys():
                query += f"\t{query_params[k][0]} ({query_params[k][1]}) : {query_params[k][3]}\n\n"

        body_params = function_info['body']
        body = ""
        if not "None" in body_params.keys():
            for k in body_params.keys():
                body += f"\t{body_params[k][0]} ({body_params[k][1]}) : {body_params[k][3]}\n\n"

        with open(path+"\\APIdocstrings.md", '+a', encoding="UTF-8") as docstrings_file:
            docstrings_file.write(title)
            docstrings_file.write(info)
            docstrings_file.write("\tclient_id (str): Client aplication id.\n\n\ttoken (str) : User oauth token.\n\n")
            docstrings_file.write(query)
            docstrings_file.write(body)
        docstrings_file.close()

    print(info)
    print(query)
    print(body)
    
    #Basics.Get_Users()

    



    
        
