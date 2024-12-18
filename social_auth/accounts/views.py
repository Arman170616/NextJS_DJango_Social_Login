import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        # Verify token with Google's OAuth API
        response = requests.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}")
        
        if response.status_code == 200:
            user_data = response.json()
            email = user_data.get("email")
            name = user_data.get("name")

            # Create or update the user
            user, created = User.objects.get_or_create(username=email, email=email)
            if created:
                user.first_name = name
                user.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
