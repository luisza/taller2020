from django.conf.urls import url
from django.urls import path
from miapp import views

urlpatterns = [
    path('', views.miindex, name="pag_principal" ),
    path('carga_csv', views.cargar_csv),
    path('csv', views.descargue_csv),
    path('hora', views.mi_vista_cacheada),
    path('autenticado', views.mi_vista_autorizada),
    url('fecha/(?P<anio>\d+)/(?P<mes>enero|febrero|marzo)/(?P<dia>\d+)/',
        views.mis_fechas),
    path('fecha/<int:anio>/<int:mes>/<int:dia>/', views.mis_fechas)
]
