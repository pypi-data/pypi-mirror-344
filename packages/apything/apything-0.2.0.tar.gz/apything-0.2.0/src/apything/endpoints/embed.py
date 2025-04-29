from ..util.http_util import HttpUtil
from ..models.embed_model import Embed


class Embed:
    def __init__(self, client):
        self.client = client  # Reference to APIClient
        self.endpoints = self.client.config['endpoints']['embed']
        self.session = self.client.session
        self.base_url = self.client.base_url
        self.headers = self.client.session.headers

    
    def get_active_embeds(self):
        url = f"{self.base_url}/{self.endpoints['embed']}"
        json_data = HttpUtil.safe_request(self.session, url, self.headers, method='GET')

        print(json_data)

        embeds = [Embed.from_json(embedItem) for embedItem in json_data['embeds']]

        return embeds