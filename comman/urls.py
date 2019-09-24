from django.urls import path, include, re_path
from rest_framework_jwt.views import verify_jwt_token
from users.views import (
    checkUser,
    registerUser,
    verifyEmail,
    Authenticate,
    userDetails,
    OAuthenticate
)


urlpatterns = [

    # Check user From USER VIEW
    path('check/user/', checkUser, name='check_user'),

    # Register user From USER VIEW
    path('register/', registerUser, name='register_user'),

    # Verify user email From USER VIEW
    re_path(
        r'^verify/email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', verifyEmail, name='verify_user_email'),

    # Authenticate user From USER VIEW
    path('authenticate/', Authenticate.as_view(), name='authenticate_user'),

    # Verify JWT Token
    path('verify/token/', verify_jwt_token),

    # User details From USER VIEW
    path('user-details/', userDetails, name='user_details'),

    # Oauth authenticate user From USER VIEW
    path('oauthenticate/', OAuthenticate.as_view(),
         name='oauthenticate_user')


]
