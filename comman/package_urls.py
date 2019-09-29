from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

# From Package VIEW
from package.views import(
    packageReadyApiCallInference,
    validateApiKey,
    activeApiList
)


urlpatterns = [
    # package PREFIX for actions used from package
    path('package/', include([
        # Ready Api Call Inference From Package VIEW
        path('call/ready/', packageReadyApiCallInference, name='ready_api_call'),
        # Validate API KEY From Package VIEW
        path('check/api-key/', validateApiKey, name='validate_api_key'),
        # Get List of Activate APIs From Package VIEW
        path('get/models/', activeApiList, name='active_api_list'),
    ])),
]
