from rest_framework.decorators import api_view
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests

@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return Response({"error": "Token is required"}, status=400)

    try:
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "984202558833-4i7fjbmtdu19qc2j7q63vfu1sso4t0as.apps.googleusercontent.com")
        user_id = idinfo['sub']
        email = idinfo.get('email')

        # Authenticate or create the user here as per your application logic
        return Response({"message": "Login successful", "data": idinfo})
    except ValueError as e:
        return Response({"error": "Invalid token"}, status=400)
