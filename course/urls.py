from django.urls import path
from . import views

urlpatterns = [
    path("course_list/", views.CourseSearchList.as_view(), name='course_list_search'),
    path("search/", views.SearchCourse.as_view(), name='search')
]