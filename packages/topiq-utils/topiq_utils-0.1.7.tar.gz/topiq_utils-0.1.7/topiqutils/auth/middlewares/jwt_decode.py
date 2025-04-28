from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import traceback

def get_params(request: Request):
    req_body = {}
    try:
        req_body = request._json
    except Exception:
        # print(e)
        pass
    query_params = request.query_params or {}
    path_params = request.path_params or {}
    params = {**req_body, **query_params, **path_params}
    return params


class JWTDecodeMiddleWare:
    def __init__(self, authenticator):
        self.authenticator = authenticator

    async def jwt_decode(
        self,
        request: Request,
        params=Depends(get_params),
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ):
        try:
            payload = await self.authenticator.decode(credentials.credentials)
            payload["token"] = credentials.credentials
            if payload.get("service_type") == "private":
                return payload
            if params.get("app_id") in payload.get("applications", []):
                return payload
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Not Authorized"
            )
        except Exception as e:
            print(traceback.print_exc())
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Not Authorized"
            )
