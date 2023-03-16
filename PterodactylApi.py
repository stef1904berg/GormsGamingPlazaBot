import json

import requests


def parse_servers(server_env: str):
    servers = server_env.replace(" ", "").split(",")
    parsed_servers = []
    for server in servers:
        parsed_servers.append(server.split("-")[0])
    return parsed_servers


class PterodactylApi:
    def __init__(self, bearer_token: str, api_url, servers=None):
        self.bearer_token = bearer_token
        self.api_url = api_url + "api/"
        if servers is None:
            self.servers = []
        self.servers = servers

        self.session = requests.session()
        self.headers = {
            "Authorization": "Bearer " + self.bearer_token
        }

    def get_server(self, server):
        response = self.session.get(self.api_url + 'client/servers/' + server, headers=self.headers)
        if response.status_code != 200:
            return None
        return response.json()

    def upload_whitelist(self, whitelist):
        for server in self.servers:
            resp = self.session.post(
                self.api_url + f"client/servers/{server}/files/write?file=whitelist.json",
                data=json.dumps(whitelist),
                headers=self.headers
            )
            print(resp.content)
            self.send_command(server, "whitelist reload")
            self.send_command(server, "whitelist list")

    def send_command(self, server, command):
        self.session.post(
            self.api_url + f"client/servers/{server}/command",
            data={"command": command},
            headers=self.headers
        )
