from django.urls import path, include, re_path
from . import views


urlpatterns = [
    # User PREFIX (Closed URLs)
    path('user/', include([
        # Profile Create URL
        # path('profile/', views.userProfileCreateAPI,
        #      name="user_profile_create"),
    ])),
]
