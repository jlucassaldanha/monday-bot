import os, json, requests, webbrowser, secrets

from dotenv import load_dotenv

from wsgiref.simple_server import make_server
from wsgiref.util import request_uri

from .src.webpage import PSEUDO_HTML
from ..error_handle import APIOAuthErrors


class Credentials():
    redirect_uri = ""
    url = ""
    client_id = ""
    client_secrets = ""
    query_url = ""

    OAUTH2_URL_BASE = "https://id.twitch.tv/oauth2"
    oauth_authorize_params = "/authorize?response_type=code&client_id={}&redirect_uri={}&scope={}&state={}"
    
    def read_credentials_file(self, credentials_json: str) -> dict:
        """
        Creates a :class:`AuthorizationCodeGrantFlow`.

        Parameters:
            credentials_json (str) : The path to the credentials.json file that have client information.  

        Returns:
            A dict of credentials data.     
        """

        # Read the credentials file data and check keys    
        with open(credentials_json, 'r') as creds_json:
            creds_data = json.load(creds_json)

        creds_json.close()

        # Verify if got the required keys in the data.
        # Case its True save the values in the variables  
        # Case its False, raise execption
        if ("client_id" in list(creds_data) and "client_secrets" in list(creds_data) 
            and "scopes" in list(creds_data) and "redirect_uri" in list(creds_data)):

            self.client_id = creds_data["client_id"]
            self.client_secrets = creds_data["client_secrets"]
            self.scopes = creds_data["scopes"]
            self.redirect_uri = creds_data["redirect_uri"]

            return creds_data

        else:
            missing_keys = ""
            for k in list(creds_data):
                if not k in ["client_id", "client_secrets", "scopes", "redirect_uri"]:
                    missing_keys += "'" + k + "', "
                    raise APIOAuthErrors("Credentials file missing keys: Verify for the keys {}.".format(missing_keys[:-2]))
    
    def read_credentials_dotenv(self) -> dict:
        load_dotenv()
        try:
            self.client_id = os.environ["CLIENT_ID"]
            self.client_secrets = os.environ["CLIENT_SECRETS"]
            self.scopes = os.environ["SCOPES"]
            self.redirect_uri = os.environ["REDIRECT_URI"]
            
            return {
                "client_id" : self.client_id,
                "client_secrets" : self.client_secrets,
                "scopes" : self.scopes,
                "redirect_uri" : self.redirect_uri
            }

        except KeyError:
            raise Exception(".env missing keys")
            
    def _localServerApp(self, environ, start_response):
        """
        Creat local server app.
        """
        status = "200 OK"
        headers = [(
            "Content-type", 
            "text/html; charset=utf-8"
            )]  
        
        start_response(status, headers)

        self.query_url = request_uri(environ)

        return PSEUDO_HTML
    
    def generate_state_key(self) -> str:
        return secrets.token_urlsafe(32)
    
    def local_server_authorization(self) -> str:
        """
        Runs a local server to got the code from teh authorization request

        Returns:
            Oauth code.
        """
        # get port and host from redirect_uri
        _i = len(self.redirect_uri) - self.redirect_uri[::-1].find(":")
        i_ = self.redirect_uri[_i:].find("/")
        port = int(self.redirect_uri[_i:][:i_])

        __i = self.redirect_uri.find("//") + 2
        i__ = len(self.redirect_uri[__i:]) - len(self.redirect_uri[_i:]) - 1
        host = self.redirect_uri[__i:][:i__]

        server = make_server(host, port, self._localServerApp)

        # Generate random statekey
        generated_state_key = self.generate_state_key()

        # Cronstruct the scopes string                
        scopes = self.scopes[0]
        for scope in self.scopes[1:]:
            scopes += "%20" + scope

        # construct the link to the authorization page.
        self.url = self.OAUTH2_URL_BASE + self.oauth_authorize_params.format(self.client_id, self.redirect_uri, scopes, generated_state_key)

        try:
            # Open the link
            webbrowser.open(self.url)
            
            # Run the server until recive a data
            server.timeout = None
            server.handle_request()

            # Get the part of the url with the parameters
            r = self.query_url

        finally:
            server.server_close()
            
            # try to find code
            i = r.find("?code=")

            # Case got a error response i will be -1
            if i == -1:
                error_i = r.find("?error=") + 7
                error_descr_i = r.find("&error_description=")
                state_key_i = r.find("&state=")
                
                error = r[error_i:error_descr_i]

                error_descr_i = error_descr_i + 19
                error_descr = r[error_descr_i:state_key_i]

                state_key_i = state_key_i + 7
                returned_state_key = r[state_key_i:]

                if returned_state_key == generated_state_key:
                    raise APIOAuthErrors("Authorization error:\n - {}: {}".format(error, error_descr))
                else:
                    raise APIOAuthErrors("Recived state key doesn't match generated state key.")
                
            else:
                scope_i = r[i:].find("&scope=")
                code_i = 6
                self.oauth_code = r[i:][code_i:scope_i] 

                state_key_i = r[scope_i:].find("&state=")

                if state_key_i != -1:
                    state_key_i = state_key_i + 7
                    returned_state_key = r[state_key_i:]

                    if returned_state_key == generated_state_key:
                        return self.oauth_code
                    else:
                        raise APIOAuthErrors("Recived state key doesn't match generated state key.")
                else:
                    raise APIOAuthErrors("Authorization doesn't returned a state key.")

class Token():
    token_file_data = ""
    access_token = ""
    refresh_token = ""

    OAUTH2_URL_BASE = "https://id.twitch.tv/oauth2"
    OAUTH2_HEADERS = {
    'Content-Type' : 
    'application/x-www-form-urlencoded'
    }
    oauth_new_token_data = "client_id={}&client_secret={}&code={}&grant_type=authorization_code&redirect_uri={}"
    oauth_refresh_token_data = "grant_type=refresh_token&refresh_token={}&client_id={}&client_secret={}"

    @classmethod
    def read_token_file(self, token_json: str) -> dict:
        """
        Read token file:

        Parameters:
            token_json (str): Path to the token json file.

        Returns:
            Token data.
        """
        # Read token
        with open(token_json, 'r') as json_file:
            self.token_file_data = json.load(json_file)
        json_file.close()
        
        # Verify if has necessary keys and save in variables
        if ("access_token" in list(self.token_file_data) and
            "refresh_token" in list(self.token_file_data) and
            "token_type" in list(self.token_file_data)):

            self.access_token = self.token_file_data["access_token"]
            self.refresh_token = self.token_file_data["refresh_token"]

            self.valid_token = self.validate_token(self.access_token)

            return self.token_file_data
        
        else:
            missing_keys = ""
            for k in list(self.token_file_data):
                if not k in ["access_token", "refresh_token", "token_type"]:
                    missing_keys += "'" + k + "', "
                    raise APIOAuthErrors("Token file missing keys: Verify for the keys {}.".format(missing_keys[:-2]))

    @classmethod
    def create_refresh_token(self, 
                             client_id: str, 
                             client_secrets: str, 
                             code: str = None, 
                             redirect_uri: str = None, 
                             refresh_token: str = None) -> dict:
        """
        Create new or refresh a token:
        
        Parameters:
            client_id (str) : Client id key from credentials.
            client_secrets (str) : Client secrets from credentials.
            code (str) = None : Code give by the authorization screen when run ´openLocalServerAuthorization´.
            redirect_uri (str) : Default = None. Uri to redirect client after authorization.
            refresh_token (str) : Default = None. Code to refresh the token.

        Save data in token.json.

        Returns:
            New token data.
        """

        # Construct links to request
        url = self.OAUTH2_URL_BASE + "/token"

        # Verify if its a token creation or refresh
        if code != None and refresh_token == None:
            data = self.oauth_new_token_data.format(client_id, client_secrets, code, redirect_uri)

        if refresh_token != None and code == None:
            data = self.oauth_refresh_token_data.format(refresh_token, client_id, client_secrets)

        r = requests.post(url, data, headers=self.OAUTH2_HEADERS)

        # Verify if request succed, case True, verify keys and so on
        # save data in the token.json file
        if r.status_code == 200:
            token_data = r.json()
            if ("access_token" in list(token_data) and 
                "refresh_token" in list(token_data) and 
                "token_type" in list(token_data)):

                with open("token.json", 'w') as token_json:
                    json.dump(token_data, token_json, indent=4)
                token_json.close()

                return token_data # return
            
        #### REVISAR ERRO PARA REFRESH TOKEN ####
            else:
                missing_keys = ""
                for k in list(self.token_file_data):
                    if not k in ["access_token", "refresh_token", "token_type"]:
                        missing_keys += "'" + k + "', "
                        raise APIOAuthErrors("Refreshed or created token file missing keys: Verify for the keys {}.".format(missing_keys[:-2]))
        else:
            if r.status_code == 400:
                error_msg = json.loads(r.content.decode())["message"]
                raise APIOAuthErrors("Failed to refresh token [status code {}]: {}".format(r.status_code, error_msg))
            else:
                error_msg = json.loads(r.content.decode())
                raise APIOAuthErrors("Failed to refresh token [status code {}]: {}".format(r.status_code, error_msg))

            """
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as error:
                error_response = r.content.decode()
                error_code = r.status_code
                msg = json.loads(error_response)["message"]
                raise APIOAuthErrors("Failed to refresh token: \n- status code {}: {}".format(error_code, msg))            
            """

    @classmethod
    def validate_token(self, token: str) -> dict:
        """
        Validate the token:

        Parameters:
            token (str): Token provided by the oauth.

        Returns:
            If token is valid, return client data, else, return False.
        """

        # URL
        url = self.OAUTH2_URL_BASE + "/validate"
        # params
        headers = {"Authorization": f"OAuth {token}"}

        r = requests.get(url, headers=headers)

        # Verify if got a response
        if r.status_code == 200:
            token_data = r.json()
            if "client_id" in list(token_data):
                return token_data
            
            else:
                raise APIOAuthErrors("Token file missing client_id key.")
            
        if r.status_code == 401:
            return False
       

# Checklist de funções:
# __init__ - OK
# _localServerApp e local_server_authorization - OK
# create_refresh_token - OK
# validate_token - OK


