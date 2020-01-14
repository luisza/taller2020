from django.urls import path
from miapp import views

urlpatterns = [
    path('', views.miindex, name="pag_principal" ),
]
