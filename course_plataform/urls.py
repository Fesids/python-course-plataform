
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import Home


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Home.as_view(), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),

    path("courses/", include("course.urls")),
    path("accounts/", include("accounts.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
