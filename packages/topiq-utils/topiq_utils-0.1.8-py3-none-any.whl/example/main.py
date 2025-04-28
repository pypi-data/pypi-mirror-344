from topiqutils.auth import JWTAuthenticator
from topiqutils.auth.middlewares import JWTDecodeMiddleWare

from fastapi import Depends, FastAPI
import asyncio

authenticator = JWTAuthenticator("https://devs.topiq.ai/auths")
jwt_decode_middleware = JWTDecodeMiddleWare(authenticator)
print("Middleware initialized", jwt_decode_middleware)

app = FastAPI()


async def startup():
    await authenticator.get_jwks()
    # print("self.public_keys", authenticator.public_keys)


app.add_event_handler("startup", startup)


@app.get("/")
async def read_root():
    await authenticator.get_jwks()
    print("self.public_keys", authenticator.public_keys)
    return {"Hello": "World"}


@app.get("/secure")
async def read_secure(user=Depends(jwt_decode_middleware.jwt_decode)):
    await authenticator.get_jwks()
    print("self.public_keys", authenticator.public_keys)
    return {"Hello": "Secure World"}
