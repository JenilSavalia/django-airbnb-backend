from django.urls import path

from . import api

urlpatterns = [
    path('', api.property_list, name='property-list'),
    path('create/', api.create_property, name='create property'),
    path('<uuid:pk>/', api.properties_detail, name='get single property'),
    path('<uuid:pk>/book/', api.book_property, name='book property'),
    path('<uuid:pk>/reservations/', api.property_reservations, name='api_property_reservations'),
    path('<uuid:pk>/toggle_favorite/', api.toggle_favorite, name='api_toggle_favorite'),


]