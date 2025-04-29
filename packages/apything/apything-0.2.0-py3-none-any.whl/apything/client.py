import requests
import yaml
import os.path
from .endpoints.documents import Documents
from .endpoints.system_settings import SystemSettings
from .endpoints.workspaces import Workspaces
from .endpoints.admin import Admin

class APIClient:
    def __init__(self, base_url, api_key, version='v1'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{base_path}/config/config.yml", "r") as config_file:
            self.config = yaml.safe_load(config_file)

        self.api_key = api_key
        self.base_url = f"{base_url}{self.config[version]}"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

        # Initialize submodules
        self.documents = Documents(self)
        self.system_settings = SystemSettings(self)
        self.workspaces = Workspaces(self)
        self.admin = Admin(self)
