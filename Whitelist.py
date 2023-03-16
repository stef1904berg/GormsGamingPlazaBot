import json
import os
import requests
import uuid


class Whitelist:
    def __init__(self, whitelist_path="./whitelist.json"):
        self.whitelist_path = whitelist_path
        self.whitelist = []
        self.load_whitelist()

    def load_whitelist(self):
        if not os.path.exists(self.whitelist_path):
            with open(self.whitelist_path, "w+") as new_whitelist_file:
                new_whitelist_file.write("[]")

        with open(self.whitelist_path, 'r+') as whitelist_file:
            file_content = whitelist_file.read()
            try:
                self.whitelist = json.loads(file_content)
            except:
                print('Cannot read config file')

    def save_whitelist(self):
        with open(self.whitelist_path, "w+") as new_whitelist_file:
            new_whitelist_file.write(json.dumps(self.whitelist))

    def get_uuid_from_player_name(self, player_name: str):
        response = requests.get('https://api.mojang.com/users/profiles/minecraft/' + player_name)
        if response.status_code != 200:
            return None

        data = response.json()
        player_uuid = str(uuid.UUID(data['id']))
        return player_uuid

    def is_whitelisted(self, player_name):
        for whitelisted in self.whitelist:
            if whitelisted['name'] == player_name:
                return True
        return False

    def get(self, player_name):
        for whitelisted in self.whitelist:
            if whitelisted['name'] == player_name:
                return whitelisted
        return None

    def add(self, player_name):
        if self.is_whitelisted(player_name):
            return True

        player_uuid = self.get_uuid_from_player_name(player_name)
        if player_uuid is None:
            return False

        self.whitelist.append({
            "uuid": player_uuid,
            "name": player_name
        })
        self.save_whitelist()

        return True

    def remove(self, player_name):
        if not self.is_whitelisted(player_name):
            return False

        to_remove = self.get(player_name)
        index_to_remove = self.whitelist.index(to_remove)
        self.whitelist.pop(index_to_remove)

        self.save_whitelist()

        return True


