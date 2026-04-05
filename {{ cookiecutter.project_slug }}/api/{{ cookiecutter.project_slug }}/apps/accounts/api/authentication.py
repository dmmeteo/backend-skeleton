from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request


class CustomSessionAuthentication(SessionAuthentication):
    def authenticate_header(self, request: Request) -> str:
        return "Session"

    def enforce_csrf(self, request: Request) -> None:
        """
        Exempt CSRF for session based authentication "application/json".
        """
        if request.content_type != "application/json":
            super().enforce_csrf(request)


class CustomSessionAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "impacttrash.apps.accounts.api.authentication.CustomSessionAuthentication"
    name = "SessionAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "sessionid",
            "description": "Session-based authentication using cookie sessions",
        }
