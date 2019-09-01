from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# router.register('profile', views.ProfileViewSet)
urlpatterns = [
    # User PREFIX (Closed URLs)
    path('user/', include([
        path('', include(router.urls)),

        # Api's Image List URL
        path('api/image/', views.ApiImageList.as_view(),
             name="user_api_image_list"),
    ])),

    # Frontend PREFIX (Closed URLs)
    path('frontend/', include([
         path('', include(router.urls)),

         # Api's Image List URL
         path('api/image/', views.TrialApiImageList.as_view(),
              name="public_api_image_list"),
         ])),
]
