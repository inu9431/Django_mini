from tokenize import TokenError

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access")
        if not access_token:
            return None
        try:
            validated_token = self.get_validated_token(access_token)
        except TokenError:
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed("유효하지 않은 토큰입니다")

        return self.get_user(validated_token), validated_token


class CookieAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'app.users.authentication.CookieAuthentication'  # 본인 경로 맞는지 확인
    name = 'CookieAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'access',
        }