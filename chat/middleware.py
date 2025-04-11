from django.contrib.auth.models import AnonymousUser  # Importação correta
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.db import database_sync_to_async
from users.models import CustomUser  # Substitua pelo seu modelo de usuário

class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_params = scope.get("query_string", b"").decode("utf-8").split("&")
        token_param = next((qp for qp in query_params if qp.startswith("token=")), None)
        token = token_param.split("=")[1] if token_param else None

        if token:
            try:
                access_token = AccessToken(token)
                user = await self.get_user(access_token)
                scope["user"] = user
            except (InvalidToken, TokenError, CustomUser.DoesNotExist):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, access_token):
        user_id = access_token["user_id"]
        return CustomUser.objects.get(id=user_id)