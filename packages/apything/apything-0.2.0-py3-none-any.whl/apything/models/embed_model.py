'''from dataclasses import dataclass


@dataclass
class Embed:
    id: int
    uuid: str
    enabled: bool
    chat_mode: str
    createdAt: str
    workspace_id: int
    workspace_name: str
    chat_count: int

    @classmethod
    def from_json(cls, json_data: dict):
        json_like_args = {
            k: json_data.get(k) for k in ('id', 'uuid', 'enabled',
                                           'chat_mode', 'createdAt', 'chat_count')
        }

        # Use unpacking for attributes that map closely to the json structure and
        # handle separately those attributes that are mapped differently
        return cls(
            **json_like_args,
            workspace_id=json_data['workspace']['id'],
            workspace_name=json_data['workspace']['name'])'''