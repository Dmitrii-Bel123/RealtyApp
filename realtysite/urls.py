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
    path('api/adverts/create/', api.create_advert, name='create_advert'),

    path('api/schema', SpectacularAPIView.as_view(), name='api_schema'),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='api_schema'), name='api_docs'),

]
