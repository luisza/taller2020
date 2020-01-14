import csv
from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from miapp.forms import MiContacto


def miindex(request):

    if request.method == 'POST':
        form = MiContacto(request.POST)
        if form.is_valid():
            print("WIIII")
    else:
        form = MiContacto()

    context = {
        'hora' : now(),
        'form': form
    }
    return render(request, 'index.html', context=context)


@cache_page(60 * 2)
def mi_vista_cacheada(request):
    hora=now()
    return HttpResponse(str(hora))

def check_user(user):
    return all([user.has_perm(perm) for perm in ('auth.delete_group', 'auth.add_group')])

@login_required
@user_passes_test(lambda x: x.has_perm('auth.delete_group'))
def mi_vista_autorizada(request):
    data = {
        'user': request.user.username
    }
    return JsonResponse(data)

def parse_int(valor):
    try:
        dev=int(valor)
    except:
        dev = 0
    return dev

def mis_fechas(request, anio, mes, dia):
    hora = parse_int(request.GET.get('hora', '0'))
    minuto = parse_int(request.GET.get('minuto', '0'))
    meses={ 'enero': 1, 'febrero': 2,   'marzo': 3, }
    anio, mes_p, dia = int(anio), parse_int(mes), int(dia)
    if mes_p == 0:
        if mes in meses:
            mes = meses[mes]
        else:
            mes = mes_p
    else:
        mes = mes_p
    if mes ==0 or dia ==0 or anio == 0:
        raise Http404("Alguna fecha es 0 o no es válida")
    data = {
        'anio': anio,
        'mes': mes,
        'dia': dia,
        'fecha': datetime(year=anio, month= mes, day=dia,
                          minute=minuto, hour=hora)
    }
    return JsonResponse(data)

def descargue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="miarchivopatito.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
