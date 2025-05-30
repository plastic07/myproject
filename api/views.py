import os
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from .models import Order
from .serializers import OrderSerializer
from google_auth_oauthlib.flow import Flow

# Allow insecure transport (for local dev only)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = 'client_secret.json'

# ✅ Match the scopes you see in the callback URL
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

REDIRECT_URI = 'http://127.0.0.1:8000/oauth2callback/'


def login(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent', include_granted_scopes='true')
    return JsonResponse({'auth_url': auth_url})


def callback(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    try:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
    except Exception as e:
        print("Token Fetch Error:", str(e))
        return JsonResponse({'error': 'Token fetch failed', 'details': str(e)}, status=400)

    credentials = flow.credentials

    response = requests.get(
        'https://www.googleapis.com/oauth2/v1/userinfo',
        params={'alt': 'json', 'access_token': credentials.token}
    )
    user_info = response.json()

    email = user_info.get('email')
    if not email:
        return JsonResponse({'error': 'Failed to retrieve email from Google'}, status=400)

    user, created = User.objects.get_or_create(username=email, defaults={'email': email})
    django_login(request, user)

    return JsonResponse({
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'email': email,
        'username': user.username,
        'is_new_user': created,
    })


@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET'])
def get_orders(request):
    token = request.headers.get('Authorization')
    if token != 'Bearer mysecrettoken':
        return Response({'error': 'Unauthorized'}, status=401)

    title = request.GET.get('title')
    orders = Order.objects.filter(title=title) if title else Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
