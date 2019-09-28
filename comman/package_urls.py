from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

# From Package VIEW
from package.views import(
    packageReadyApiCallInference,
)


urlpatterns = [
    # package PREFIX for actions used from package
    path('package/', include([
        # Ready Api Call Inference From Package VIEW
        path('call/ready/', packageReadyApiCallInference, name='ready_api_call'),
    ])),
]
