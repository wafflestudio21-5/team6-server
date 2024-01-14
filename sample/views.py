from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


# GET 요청 테스트 위한 View
class ConnectionCheckAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        return Response({"message": "Success"}, status=status.HTTP_200_OK)

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        return Response({"message": refresh_token}, status=status.HTTP_200_OK)
