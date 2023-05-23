from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.room_create, name='room-create'),
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),

]