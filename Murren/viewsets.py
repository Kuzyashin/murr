from rest_framework.views import APIView
from rest_framework.response import Response

from Murren.serializers import MyMurrenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class CurrentUserView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = MyMurrenSerializer(request.user)
        return Response(serializer.data)