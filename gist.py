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

    def create(self, filenames, description, public=True, anonymous=False):
        files = {}
        for filename in filenames:
            with open(filename, 'r') as f:
                files.setdefault(filename, {})['content'] = f.read()

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

    def edit(self, id, filenames, description):
        files = {}
        for filename in filenames:
            with open(filename, 'r') as f:
                files.setdefault(filename, {})['content'] = f.read()

        url = 'https://api.github.com/gists/{id}'.format(id=id)
        data = {
            "description": description,
            "files": files
        }

        r = requests.patch(url, json=data, auth=HTTPBasicAuth(self.username, self.auth_token))
        content = json.loads(r.content)

        gist_url = 'https://gist.github.com/{username}/{id}'
        return gist_url.format(username=self.username, id=content['id'])

    def delete(self, id):
        url = 'https://api.github.com/gists/{id}'.format(id=id)
        requests.delete(url, auth=HTTPBasicAuth(self.username, self.auth_token))


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


@cli.command()
@click.argument('id', nargs=1)
@click.argument('files', nargs=-1)
@click.argument('description', nargs=1)
def edit(id, files, description):
    '''python gist.py edit id file1 file2 description'''
    print client.edit(id, files, description)


@cli.command()
@click.argument('id', nargs=1)
def delete(id):
    '''python gist.py delete id'''
    client.delete(id)


cli()
