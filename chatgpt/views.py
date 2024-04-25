from rest_framework.decorators import api_view
from .bots import translate_bot
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class TranslateAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message")
        chatgpt_response = translate_bot(user_message)
        return Response({"message": chatgpt_response})
