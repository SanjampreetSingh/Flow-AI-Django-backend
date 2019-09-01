from django.urls import path, include, re_path
from . import views


urlpatterns = [
    # User PREFIX
    path('user/', include([

        # Api's List
        path('api/', views.ApiList.as_view(), name="user_api_list"),

        # Api's Image List
        path('api/image/', views.ApiImageList.as_view(),
             name="user_api_image_list"),

        # Api's Retrieve
        re_path(r'api/detail/(?P<pk>\d+)$',
                views.ApiRetrieve.as_view(), name="user_api_retrieve"),

        # Api Category
        path('api/category/list/', views.ApiCategoryList.as_view(),
             name='api_category_list'),
    ])),

    # Frontend PREFIX
    path('frontend/', include([
        # Api's Image List
        path('api/image/', views.TrialApiImageList.as_view(),
             name="public_api_image_list"),

        # Api's List
        path('api/', views.TrialApiList.as_view(), name="public_api_list"),

        # Api's Retrieve
        re_path(r'api/(?P<pk>\d+)/detail/$',
                views.TrialApiRetrieve.as_view(), name="public_api_retrieve"),

        # Api Category
        path('api/category/list/', views.TrailApiCategoryList.as_view(),
             name='api_category_list_frontend'),
    ])),
]
