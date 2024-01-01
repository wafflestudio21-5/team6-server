from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# GET 요청 테스트 위한 View
class ConnectionCheckAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Success"}, status=status.HTTP_200_OK)
