import os

from .twitch_oauth.auth_code_grant_flow import Credentials, Token
from .error_handle import APIOAuthErrors

class OAuth(Credentials):
    
    def credentials(self, credentials_file: str) -> None:  
        if os.path.exists(credentials_file):
            self.read_credentials_file(credentials_file)

            print("Read Credentials")
        else:
            raise APIOAuthErrors("Credentials json file not found")
        
    def dotenv_credentials(self) -> None:
        self.read_credentials_dotenv()
        
    def access_token(self, token_file: str) -> None:
        token_file_data = None

        if os.path.exists(token_file):
            print("Read Token")
        
            token_file_data = Token.read_token_file(token_file)
        
            if not Token.valid_token:
                print("Refresh Token")
                try:
                    token_file_data = Token.create_refresh_token(self.client_id, self.client_secrets, refresh_token=token_file_data['refresh_token'])
                except APIOAuthErrors:
                    print("Create Token")
                    code = self.local_server_authorization()
                    
                    token_file_data = Token.create_refresh_token(self.client_id, self.client_secrets, code=code, redirect_uri=self.redirect_uri)

        if not token_file_data:
            print("Create Token")
            code = self.local_server_authorization()
            
            token_file_data = Token.create_refresh_token(self.client_id, self.client_secrets, code=code, redirect_uri=self.redirect_uri)

        self.token = token_file_data["access_token"]
