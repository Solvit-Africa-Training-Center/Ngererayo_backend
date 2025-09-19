# chat/middleware.py
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode
from django.conf import settings

@database_sync_to_async
def get_user(validated_token):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user_id = validated_token["user_id"]
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def _call_(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token")
        if token:
            try:
                validated_token = UntypedToken(token[0])
                scope["user"] = await get_user(jwt_decode(token[0], settings.SECRET_KEY, algorithms=["HS256"]))
            except Exception:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super()._call_(scope, receive, send)