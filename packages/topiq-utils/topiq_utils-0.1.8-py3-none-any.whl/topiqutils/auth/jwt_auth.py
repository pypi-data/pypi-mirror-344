import json
import jwt
from jwt.algorithms import RSAAlgorithm
import requests
from topiqutils.auth import jwks_fetched
import asyncio


class JWTAuthenticator:

    def __init__(self, jwks_origin, jwks_path="/.well-known/jwks.json"):
        self.public_keys = {}
        self.jwks_origin = jwks_origin
        self.jwks_path = jwks_path
        self.jwks_url = f"{self.jwks_origin}{self.jwks_path}"
        asyncio.run(self.get_jwks())

    async def get_jwks(self):
        global jwks_fetched
        try:
            with requests.get(self.jwks_url) as response:
                jwks = response.json()
                jwks_fetched = True
                print("JWKS fetched successfully")
                for jwk in jwks["keys"]:
                    kid = jwk["kid"]
                    self.public_keys[kid] = RSAAlgorithm.from_jwk(json.dumps(jwk))
        except requests.exceptions.JSONDecodeError as e:
            print(
                f"Error decoding JWKS JSON. Fetched content is not a proper JSON. Either the URL is incorrect or the server is down. \nPlease check if the url: {self.jwks_url} is correct and the server is up.",
            )
        except requests.exceptions.ConnectionError as e:
            print(
                f"Error connecting to JWKS URL. Either the URL is incorrect or the server is down. \nPlease check if the url: {self.jwks_url} is correct and the server is up.",
            )
        except requests.RequestException as e:
            print(type(e))
            print("Error fetching JWKS:", e)

    async def decode(self, token):
        try:
            unverified_headers = jwt.get_unverified_header(token)
            decoded_token = jwt.decode(
                token,
                self.public_keys[unverified_headers["kid"]],
                algorithms=[unverified_headers["alg"]],
                audience="Auth Service",
            )
            return decoded_token

        except jwt.PyJWTError as e:
            import traceback

            traceback.print_exc()
