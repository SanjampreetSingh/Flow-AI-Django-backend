from django.urls import path, include, re_path
from . import views


urlpatterns = [
    # ready PREFIX
    path('ready/', include([

        # Ready Api's List
        path('api/', views.ReadyApiList.as_view(), name="ready_api_list"),

        # Ready Api's Media List
        path('api/media/', views.ReadyApiMediaList.as_view(),
             name="ready_api_image_list"),

        # Ready Api's Retrieve
        re_path(r'api/detail/(?P<pk>\d+)$',
                views.ReadyApiRetrieve.as_view(), name="ready_api_retrieve"),

        # Ready Api Category
        path('api/category/list/', views.ReadyApiCategoryList.as_view(),
             name='ready_api_category_list'),
    ])),

]
