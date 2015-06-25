# Author: Jan Margeta <jmargeta@gmail.com>
#
# (c) 2015
#
# License: MIT

import requests
import json
import os

from posixpath import join as urljoin
from requests_oauthlib import OAuth1Session
import xmltodict


CLIENT_ID = os.getenv('GOODREADS_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOODREADS_CLIENT_SECRET')
OAUTH_TOKEN_JSON = os.getenv(
    'GOODREADS_OAUTH_TOKEN_JSON', './goodreads_oauth.json')

req_token_url = 'https://www.goodreads.com/oauth/request_token'
authorize_url = 'https://www.goodreads.com/oauth/authorize'
access_token_url = 'https://www.goodreads.com/oauth/access_token'


class GoodreadsClient(object):
    def __init__(self):
        """Authenticate user with saved credentials.

        GoodreadsClient.authorize_access()
        must be called the very first time
        """
        # relogin with the saved credentials
        with open(OAUTH_TOKEN_JSON, 'r') as fp:
            access_token = json.load(fp)

        self.session = OAuth1Session(
            CLIENT_ID,
            client_secret=CLIENT_SECRET,
            resource_owner_key=access_token['oauth_token'],
            resource_owner_secret=access_token['oauth_token_secret'])

        self.user = self.auth_user

    @staticmethod
    def authorize_access():
        """Authorize the app on Goodreads to access user data.

        Run this once before doing anything else.
        """

        goodreads = OAuth1Session(CLIENT_ID, client_secret=CLIENT_SECRET)
        oauth_token = goodreads.fetch_request_token(req_token_url)
        authorize_url = goodreads.authorization_url(authorize_url)

        raw_input("""Visit the following link to approve the app:
        -----------------------------------------------------
        {}
        -----------------------------------------------------
        Press Return when done
        """.format(authorize_url))

        # fetch oauth access token
        # the verifier needs somevalue, probably any will do
        access_token = goodreads.fetch_access_token(access_token_url,
                                                    verifier=u'y')

        with open(OAUTH_TOKEN_JSON, 'w') as fp:
            json.dump(access_token, fp)

        return access_token

    @staticmethod
    def parse_response(goodreads_response):
        return xmltodict.parse(goodreads_response.content)['GoodreadsResponse']

    def get(self, what, **params):
        """Calling the API"""
        url = urljoin('https://goodreads.com', what)
        return self.session.get(url, params=params)

    @property
    def auth_user(self):
        user_req = self.get('api/auth_user')
        user = GoodreadsClient.parse_response(user_req)['user']
        return user

    @property
    def owned_books(self):
        books_req = self.get(
            'owned_books/user',
            id=self.user['@id'],
            format='xml')
        parsed = GoodreadsClient.parse_response(books_req)
        return parsed['owned_books']['owned_book']

    @property
    def user_shelves(self):
        shelves_req = self.get('shelf/list.xml', user_id=self.user['@id'])
        user_shelves = GoodreadsClient.parse_response(
            shelves_req)['shelves']['user_shelf']
        return user_shelves
