from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# router.register('profile', views.ProfileViewSet)
urlpatterns = [
    # User PREFIX
    path('user/', include([
        path('', include(router.urls)),

        # Api's Image List
        path('api/image/', views.ApiImageList.as_view(),
             name="user_api_image_list"),
    ])),

    # Frontend PREFIX
    path('frontend/', include([
         path('', include(router.urls)),

         # Api's Image List
         path('api/image/', views.TrialApiImageList.as_view(),
              name="public_api_image_list"),

         # Api's List
         path('api/', views.TrialApiList.as_view(), name="public_api_list"),

         # Api's Retrieve
         re_path(r'api/(?P<pk>\d+)/detail/$',
                 views.TrialApiRetrieve.as_view(), name="public_api_retrieve"),

         ])),
]
