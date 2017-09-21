import os
import json

import requests
from requests.auth import HTTPBasicAuth


class GistClient(object):

    def __init__(self):
        try:
            with open(os.path.expanduser('~/.github_token'), 'r') as f:
                username, auth_token = f.read().strip().split('\n')
        except:
            username, auth_token = 'anonymous', ''
        finally:
            self.username, self.auth_token = username, auth_token

    def gets(self):
        pass

    def get(self, id):
        pass

    def create(self, file_names, description, public=True, anonymous=False):
        if (not anonymous) and (not self.auth_token):
            anonymous = True

        files = {}
        for file_name in file_names:
            with open(file_name, 'r') as f:
                files.setdefault(file_name, {})['content'] = f.read()

        url = 'https://api.github.com/gists'
        data = {
            "description": "the description for this gist",
            "public": public,
            "files": files
        }

        if not anonymous:
            r = requests.post(url, json=data, auth=HTTPBasicAuth(self.username, self.auth_token))
        else:
            r = requests.post(url, json=data)

        content = json.loads(r.content)

        gist_url = 'https://gist.github.com/{username}/{id}'
        return gist_url.format(username=self.username if not anonymous else 'anonymous', id=content['id'])

    def edit(self):
        pass

    def delete(self):
        pass


if __name__ == '__main__':
    client = GistClient()
    r = client.create(['requirements.txt'], 'test', public=True, anonymous=False)
