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
from apps.views import (
    AppsView
)
# From READY API VIEW
from readyApis.views import (
    ReadyApiList,
    ReadyApiRetrieve,
    ReadyApiMediaList,
    ReadyApiCategoryList,
    readyApiDemo
)
# From MODULES VIEW
from modules.views import (
    ModuleList,
    ModuleDetails
)
# From READY API USAGES VIEW
from readyApiUsages.views import (
    ReadyApiUsageBucketsRetrieve
)
# From READY APP VIEW
from readyApps.views import (
    addReadyApiToApp
)

# Router for app PREFIX
apps_router = DefaultRouter()

# App ViewSet From App VIEW
apps_router.register('app', AppsView)


urlpatterns = [

    # Check user From USER VIEW
    path('check/user/', checkUser, name='check_user'),

    # Register user From USER VIEW
    path('register/', registerUser, name='register_user'),

    # Authenticate user From USER VIEW
    path('authenticate/', Authenticate.as_view(), name='authenticate_user'),

    # Verify user email From USER VIEW
    path('verify/email/', verifyEmail, name='verify_user_email'),

    # Verify JWT Token
    path('verify/token/', verify_jwt_token),

    # User details From USER VIEW
    path('user-details/', userDetails, name='user_details'),

    # Oauth authenticate user From USER VIEW
    re_path(r'^oauthenticate/(?P<provider>[A-Za-z_\-]+)/(?P<access_token>[0-9A-Za-z_\-]+)/$', OAuthenticate.as_view(),
            name='oauthenticate_user'),


    # Modules list From MODULES VIEW
    path('module/', ModuleList.as_view(), name="module_list"),

    # Modules details From MODULES VIEW
    re_path(r'^module/(?P<reference_url>[-\w]+)/$',
            ModuleDetails.as_view(), name="module_details"),

    # User PREFIX for actions used by users
    path('user/', include([
        # Default Router for app PREFIX
        path('', include(apps_router.urls)),
        # Default Router for usage-ready-api PREFIX
        re_path(r'^usage-ready-api/(?P<app>[-\w]+)/$',
                ReadyApiUsageBucketsRetrieve.as_view(), name="ready_api_usage_buckets_retrieve"),
        # Add ReadyApi To App From READY APP VIEW
        path('ready/app/activate/', addReadyApiToApp),

    ])),

    # ready PREFIX for actions used from READY API's
    path('ready/', include([
        # Ready Api's List From READY API VIEW
        path('api/', ReadyApiList.as_view(), name="ready_api_list"),

        # Ready Api's Retrieve From READY API VIEW
        re_path(r'api/(?P<reference_url>[-\w]+)/$', ReadyApiRetrieve.as_view(),
                name="ready_api_retrieve"),

        # Ready Api's Media List From READY API VIEW
        path('api-media/', ReadyApiMediaList.as_view(),
             name="ready_api_image_list"),

        # Ready Api Category List From READY API VIEW
        path('api-category/', ReadyApiCategoryList.as_view(),
             name='ready_api_category_list'),

        # Ready Api Demo From READY API VIEW
        path('demo/', readyApiDemo, name='ready_api_category_list'),
    ])),

]
