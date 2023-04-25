from django.urls import path
from . import views
urlpatterns =[
    path("detail/", views.ProfileDetail.as_view(), name="profile_detail"),
    path("update/", views.ProfileDetailUpdate.as_view(), name="profile_update")
]