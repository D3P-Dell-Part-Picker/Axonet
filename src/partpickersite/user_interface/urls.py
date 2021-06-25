from django.urls import path

from . import views

urlpatterns = [

    path('', views.part_selector, name='part_selector'),
    path('data', views.load_data, name='load_data'),
    path('map/<str:selected_parts>/', views.load_map, name='selected_parts'),
    path('map/<str:selected_parts>/reset_led/', views.reset_led, name='reset_led'),
    path('map/<str:selected_parts>/reset_led', views.reset_led, name='reset_led'),
    path('map', views.load_map, name='load_map'),
    path('reset_led/', views.reset_led, name='reset_led'),
    path('reset_led', views.reset_led, name='reset_led')

]
