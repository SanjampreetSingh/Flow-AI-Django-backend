from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import verify_jwt_token
# From USER VIEW
from users.views import (
    checkUser,
    registerUser,
    verifyEmail,
    Authenticate,
    userDetails,
    OAuthenticate
)
# From APPS VIEW
from apps.views import(
    Apps
)
# From READY API VIEW
from readyApis.views import(
    ReadyApiList,
    ReadyApiRetrieve,
    ReadyApiMediaList,
    ReadyApiCategoryList,
    readyApiDemo
)
# From MODULES VIEW
from modules.views import(
    ModuleList,
    ModuleDetails
)


# Router for User PREFIX
users_router = DefaultRouter()

# App ViewSet From App VIEW
users_router.register('app', Apps)


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
    path('oauthenticate/', OAuthenticate.as_view(), name='oauthenticate_user'),

    # Modules list From MODULES VIEW
    path('module/', ModuleList.as_view(), name="module_list"),

    # Modules datails From MODULES VIEW
    re_path(r'^module/(?P<reference_url>[-\w]+)/$',
            ModuleDetails.as_view(), name="module_details"),

    # User PREFIX for actions used by users
    path('user/', include([
        # Default Router for USER PREFIX
        path('', include(users_router.urls)),
    ])),

    # ready PREFIX for actions used from READY API's
    path('ready/', include([
        # Ready Api's List From READY API VIEW
        path('api/', ReadyApiList.as_view(), name="ready_api_list"),

        # Ready Api's Retrieve From READY API VIEW
        re_path(r'api/(?P<pk>\d+)$', ReadyApiRetrieve.as_view(),
                name="ready_api_retrieve"),

        # Ready Api's Media List From READY API VIEW
        path('api-media/', ReadyApiMediaList.as_view(),
             name="ready_api_image_list"),

        # Ready Api Category List From READY API VIEW
        path('api-category/', ReadyApiCategoryList.as_view(),
             name='ready_api_category_list'),

        # Ready Api Demo From READY API VIEW
        path('api/demo', readyApiDemo, name='ready_api_category_list'),
    ])),

]
