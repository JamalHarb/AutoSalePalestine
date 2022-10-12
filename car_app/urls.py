from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('check_register', views.check_register),
    path('check_login', views.check_login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('my_cars', views.my_cars),
    path('add_car', views.add_car),
    path('car/new', views.create_car),
    path('car/<int:id>/view', views.view_car),
    path('car/<int:id>/edit', views.edit_car),
    path('car/<int:id>/update', views.update_car),
    path('goback/<int:id>', views.goback),
    path('car/<int:id>/delete', views.delete_car),
    path('car/search', views.search_car),
]