from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class HelloWorld(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        return Response({"status": "hello world"})
