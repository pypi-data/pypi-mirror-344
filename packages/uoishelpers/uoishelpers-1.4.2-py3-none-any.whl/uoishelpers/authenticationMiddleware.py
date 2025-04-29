import os
from typing import Any
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError
)
from starlette.middleware.authentication import AuthenticationMiddleware
import aiohttp
import jwt
import json
import logging

JWTPUBLICKEY = "http://localhost:8000/oauth/publickey"
JWTRESOLVEUSERPATH = "http://localhost:8000/oauth/userinfo"

class BasicAuthBackend(AuthenticationBackend):
    def __init__(self, 
        JWTPUBLICKEY = JWTPUBLICKEY,
        JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH
        ) -> None:

        # super().__init__()
        self.publickey = None
        self.JWTPUBLICKEY = JWTPUBLICKEY
        self.JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH

    async def getPublicKey(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.JWTPUBLICKEY) as resp:
                print(resp.status)
                if resp.status != 200:
                    raise AuthenticationError("Public key not available")

                # publickey = await resp.read()
                publickey = await resp.text()
        self.publickey = publickey.replace('"', '').replace('\\n', '\n')
        print('got key', self.publickey)
        self.publickey = self.publickey.encode()
        return self.publickey

    async def authenticate(self, conn):
        print("# BEGIN #######################################")
        client = conn.client
        headers = conn.headers
        cookies = conn.cookies
        url = conn.url
        base_url = conn.base_url
        uri = url.path
        conn.url.path
        logging.debug(f'{base_url} {client}, {headers}, {cookies}')
        logging.debug(f'{uri}')
        print(f'{base_url} {client}, {headers}, {cookies}')
        print(f'{uri}')        
        
        # 1. ziskat jwt (cookies authorization nebo header Authorization: Bearer )
        jwtsource = cookies.get("authorization", None)
        if jwtsource is None:
            jwtsource = headers.get("Authorization", None)
            if jwtsource is not None:
                [_, jwtsource] = jwtsource.split("Bearer ")
            else:
                #unathorized
                pass

        print('got jwtsource', jwtsource)
        if jwtsource is None:
            raise AuthenticationError("missing code")

        # 2. ziskat verejny klic (async request to authority)
        publickey = self.publickey
        if publickey is None:
            publickey = await self.getPublicKey()
        
        # 3. overit jwt (lokalne)
        for i in range(2):
            try:
                jwtdecoded = jwt.decode(jwt=jwtsource, key=publickey, algorithms=["RS256"])
                break
            except jwt.InvalidSignatureError as e:
                # je mozne ulozit key do cache a pri chybe si key ziskat (obnovit) a provest revalidaci
                print(e)
            if (i == 1):
                # klic byl aktualizovan a presto doslo k vyjimce
                raise AuthenticationError("Invalid signature")
            
            # aktualizace klice, predchozi selhal
            publickey = await self.getPublicKey()
            print('publickey refreshed', publickey)
        
        print('got jwtdecoded', jwtdecoded)

        # 3A. pokud jwt obsahuje user.id, vzit jej primo
        user_id = jwtdecoded.get("user_id", None)
        print("some user?", user_id)
        userinfo = {"id": user_id}
        # 4. pouzit jwt jako parametr pro identifikaci uzivatele u autority
        if user_id is None:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {jwtdecoded['access_token']}"}
                async with session.get(self.JWTRESOLVEUSERPATH, headers=headers) as resp:
                    print(resp.status)
                    assert resp.status == 200
                    userinfo = await resp.json()
                    print("got userinfo", userinfo)
                    user_id = userinfo["id"]

        logging.debug(f"We know that user is {user_id}")

        if user_id is None:
            raise AuthenticationError(f"Unknown user")
            
        print("# SUCCESS #######################################")
        return AuthCredentials(["authenticated"]), userinfo
    
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response, RedirectResponse

class BasicAuthenticationMiddleware302(AuthenticationMiddleware):
    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        where = conn.url.path
        return RedirectResponse(f"/oauth/login2?redirect_uri={where}", status_code=302)

class BasicAuthenticationMiddleware404(AuthenticationMiddleware):
    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        where = conn.url.path
        return PlainTextResponse(f"Unauthorized for {where}", status_code=404)

from pydantic import BaseModel
import aiohttp
import json
import jwt
from fastapi import Request
from starlette.responses import JSONResponse
from starlette.authentication import AuthenticationError

class Item(BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

apolloQuery = "query __ApolloGetServiceDefinition__ { _service { sdl } }"
graphiQLQuery = "\n query IntrospectionQuery {\n __schema {\n \n queryType { name }\n mutationType { name }\n subscriptionType { name }\n types {\n ...FullType\n }\n directives {\n name\n description\n \n locations\n args(includeDeprecated: true) {\n ...InputValue\n }\n }\n }\n }\n\n fragment FullType on __Type {\n kind\n name\n description\n \n fields…name\n ofType {\n kind\n name\n ofType {\n kind\n name\n ofType {\n kind\n name\n ofType {\n kind\n name\n ofType {\n kind\n name\n ofType {\n kind\n name\n }\n }\n }\n }\n }\n }\n }\n }\n "
JWTPUBLICKEYURL = "http://localhost:8000/oauth/publickey"
JWTRESOLVEUSERPATHURL = "http://localhost:8000/oauth/userinfo"

def createAuthentizationSentinel(
        queriesWOAuthentization = [apolloQuery, graphiQLQuery],
        JWTPUBLICKEY = JWTPUBLICKEYURL,
        JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATHURL,
        onAuthenticationError = lambda item: JSONResponse(f"{item} unauthorized")
):
    class Sentinel:
        def __init__(self,
            JWTPUBLICKEY = JWTPUBLICKEY,
            JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH):
            self.JWTPUBLICKEY = JWTPUBLICKEY
            self.JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH
            self.publickey = None

        async def __call__(self, request: Request, item: Item) -> Any:
            try:
                await self.authenticate(request=request)
            except:
                if item.query in queriesWOAuthentization:
                    logging.info(f"Sentinel advice: this is free access to \n {item.query}")
                    return None
                logging.info(f"Sentinel advice: unauthorized access to \n {item.query}")
                return onAuthenticationError(item) 
            logging.info(f"Sentinel advice: ok access to \n {item.query}")
            pass

        async def getPublicKey(self):
            logging.debug(f"Sentinel getting public key on \n {self.JWTPUBLICKEY}")
            async with aiohttp.ClientSession() as session:
                async with session.get(self.JWTPUBLICKEY) as resp:
                    print(resp.status)
                    logging.debug(f"response from oauth authority: status {resp}")
                    if resp.status != 200:
                        raise AuthenticationError("Public key not available")

                    # publickey = await resp.read()
                    publickey = await resp.text()
                    logging.debug(f"Sentinel has got public key \n {publickey}")
            self.publickey = publickey.replace('"', '').replace('\\n', '\n')
            print('got key', self.publickey)
            self.publickey = self.publickey.encode()
            return self.publickey

        async def authenticate(self, request: Request):
            print("# BEGIN #######################################")
            client = request.client
            headers = request.headers
            cookies = request.cookies
            url = request.url
            base_url = request.base_url
            uri = url.path
            request.url.path
            logging.debug(f'Sentinel authentication phase message: \n {base_url} {client}, {headers}, {cookies}')
            logging.debug(f'{uri}')
            print(f'{base_url} {client}, {headers}, {cookies}')
            print(f'{uri}')        
            
            logging.debug(f'1. ziskat jwt (cookies authorization nebo header Authorization: Bearer )')
            # 1. ziskat jwt (cookies authorization nebo header Authorization: Bearer )
            jwtsource = cookies.get("authorization", None)
            if jwtsource is None:
                jwtsource = headers.get("Authorization", None)
                if jwtsource is not None:
                    [_, jwtsource] = jwtsource.split("Bearer ")
                else:
                    #unathorized
                    pass

            logging.debug(f'Sentinel authentication phase message: token: \n {jwtsource}')
            # print('Sentinel got jwtsource', jwtsource, "\n", self.publickey)
            logging.debug(30*"#")
            if jwtsource is None:
                logging.debug(f'Sentinel authentication phase message: TOKEN IS MISSING')
                raise AuthenticationError("missing code")
            request.scope["jwt"] = jwtsource

            # 2. ziskat verejny klic (async request to authority)
            logging.debug("2. ziskat verejny klic (async request to authority)")
            publickey = self.publickey
            if publickey is None:
                publickey = await self.getPublicKey()
            logging.debug(30*"#")
            logging.debug(f'have public key')
            print(f'have public key')

            # 3. overit jwt (lokalne)
            for i in range(2):
                try:
                    jwtdecoded = jwt.decode(jwt=jwtsource, key=publickey, algorithms=["RS256"])
                    break
                except jwt.InvalidSignatureError as e:
                    # je mozne ulozit key do cache a pri chybe si key ziskat (obnovit) a provest revalidaci
                    print(e)
                    if (i == 1):
                        # klic byl aktualizovan a presto doslo k vyjimce
                        raise AuthenticationError("Invalid signature")
                except Exception as e:
                    print(f"unexpected exception {e}")
                
                # aktualizace klice, predchozi selhal
                publickey = await self.getPublicKey()
                print('publickey refreshed', publickey)
            
            print('got jwtdecoded', jwtdecoded)
            logging.debug(f'got jwtdecoded {jwtdecoded}')
            # 3A. pokud jwt obsahuje user.id, vzit jej primo
            logging.debug("3A. pokud jwt obsahuje user.id, vzit jej primo")
            user_id = jwtdecoded.get("user_id", None)
            print("some user?", user_id)

            # 4. pouzit jwt jako parametr pro identifikaci uzivatele u autority
            if user_id is None:
                logging.debug(f"4. pouzit jwt jako parametr pro identifikaci uzivatele u autority {self.JWTRESOLVEUSERPATH}")
                async with aiohttp.ClientSession() as session:
                    headers = {"Authorization": f"Bearer {jwtdecoded['access_token']}"}
                    async with session.get(self.JWTRESOLVEUSERPATH, headers=headers) as resp:
                        logging.debug(f"Autority response {resp}")
                        print(resp.status)
                        assert resp.status == 200
                        userinfo = await resp.json()
                        logging.debug(f"Autority response user is {userinfo}")
                        print("got userinfo", userinfo)
                        user_id = userinfo["id"]

            # demouser = os.getenv("DEMOUSER", '{"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "name": "John", "surname": "Newbie"}')
            # user = json.loads(demouser)
            # if user_id is None:
            #     user["id"] = user_id
                
            logging.debug(f"We know that user is {user_id}")
            try:
                request.scope["user"] = {"id": user_id}
            except Exception as e:
                logging.debug(f"WTF {e}")
            print("# SUCCESS #######################################")
            if user_id is None:
                raise AuthenticationError(f"Unknown user")
            return None
    return Sentinel()