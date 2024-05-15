from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('table/', views.table, name='table'),
    path('graph/', views.graph, name='graph'),
    path('table/create/', views.create, name='create'),
    path('table/edit/<int:id>', views.edit, name='edit'), 
    path('table/delete/<int:id>', views.delete, name='delete'),
]
