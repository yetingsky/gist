# coding: utf8

import os
import json

import requests
import click
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
        files = {}
        for file_name in file_names:
            with open(file_name, 'r') as f:
                files.setdefault(file_name, {})['content'] = f.read()

        url = 'https://api.github.com/gists'
        data = {
            "description": description,
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


client = GistClient()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('files', nargs=-1)
@click.argument('description', nargs=1)
@click.option('--public/--no-public', default=True)
@click.option('--anonymous/--no-anonymous', default=False)
def create(files, description, public, anonymous):
    '''python gist.py create file1 file2 description --no-public --anonymous'''
    print client.create(files, description, public, anonymous)


cli()
