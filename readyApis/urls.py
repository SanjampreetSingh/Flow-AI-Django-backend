from django.urls import path, include, re_path
from . import views


urlpatterns = [
    # ready PREFIX
    path('ready/', include([

        # Ready Api's List
        path('api/', views.ReadyApiList.as_view(), name="ready_api_list"),

        # Ready Api's Retrieve
        re_path(r'api/(?P<pk>\d+)$',
                views.ReadyApiRetrieve.as_view(), name="ready_api_retrieve"),

        # Ready Api's Media List
        path('api-media/', views.ReadyApiMediaList.as_view(),
             name="ready_api_image_list"),

        # Ready Api Category List
        path('api-category/', views.ReadyApiCategoryList.as_view(),
             name='ready_api_category_list'),

        # Ready Api Demo
        path('api/demo', views.readyApiDemo,
             name='ready_api_category_list'),

    ])),

]
