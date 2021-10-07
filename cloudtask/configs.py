from django.conf import settings
from cloudtask.exceptions import CloudTaskException as Err

DCT_SECRET_HEADER_KEY: str = 'X-DCT-SECRET'
DCT_SECRET_HEADER_NAME: str = 'HTTP_X_DCT_SECRET'
DEFAULTS: dict = {
    'URL': None, # Default URL target to handle tasks,
    'SAE': None, # Service Account Email Used for HTTP authentication
    'SECRET': None, # Secreve key to validate incomes request
    'PROJECT': None, # Google Task Queue related project id
    'LOCATION': None, # Google Task Queue Location,
    'QUEUE_NAME': None # default queue name
}

class CloudTaskSettings:

    __defaults: dict

    def __init__(self, defaults: dict = None, user_settings: dict = None) -> None:
        if user_settings:
            self.__settings = user_settings
        self.__defaults = defaults or DEFAULTS

    @property
    def settigs(self) -> dict:
        if not hasattr(self, '__settings'):
            return getattr(settings, 'CLOUDTASK', {})
        return self.__settings
    
    def validate(self):
        """configurations validation"""
        for attr in dir(self):
            if 'validate_' in attr:
                getattr(self, attr)()
    
    def validate_sae(self):
        """validate service account email"""
        if not self.SAE:
            raise Err('Service account e-mail is not defined!')
    
    def validate_project(self):
        if not self.PROJECT:
            raise Err('Project ID is not defined!')
    
    def validate_location(self):
        if not self.LOCATION:
            raise Err('Location is not defined!')
    
    def get_default_queue_name(self, raise_exception=True) -> str:
        if not (name := self.QUEUE_NAME) and raise_exception:
            raise Err(
                'Default queue name not defined. '
                'Explicitly define on task decorator or in CLOUDTASK settings')
        return name
    
    def get_url(self, raise_exception=True) -> str:
        if not (url := self.URL) and raise_exception:
            raise Err(
                'Default task handler URL not defined. '
                'Explicitly define on task decorator or in CLOUDTASK settings')
        return url

    def __getattr__(self, attr: str):

        if attr not in self.__defaults:
            raise AttributeError("Invalid CLOUDTASK setting: '%s'" % attr)
        
        try:
            value = self.settigs[attr]
        except KeyError:
            value = self.__defaults[attr]

        setattr(self, attr, value)
        return value


conf = CloudTaskSettings()