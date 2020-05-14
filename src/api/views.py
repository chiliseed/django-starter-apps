import structlog
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


logger = structlog.get_logger(__name__)


class HelloWorld(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        logger.info("Greeting the world", open="any")
        return Response({"status": "hello world"})
