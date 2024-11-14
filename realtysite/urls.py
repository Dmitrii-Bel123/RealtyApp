"""
URL configuration for realtysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from realty import views
from realty import api
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout', views.logout_view, name='logout'),
    path('advert', views.advert, name='advert'),
    path('streets', views.streets, name='streets'),
    path('add_street', views.add_street, name='add_street'),
    re_path('edit_street/(?P<street_id>\d+)', views.edit_street, name='edit_street'),
    path('filter', views.filter, name='filter'),
    re_path('show_advert/(?P<advert_id>\d+)', views.show_advert, name='show_advert'),
    path('admin/', admin.site.urls),

    path('api/adverts', api.adverts, name='api_adverts'),
    path('api/schema', SpectacularAPIView.as_view(), name='api_schema'),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='api_schema'), name='api_docs'),
]
