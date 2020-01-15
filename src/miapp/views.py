import csv
from datetime import datetime
import time
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from miapp.forms import MiContacto, CSVForm
from miapp.models import TypeAggression, Region, District, Municipality, Victim, Aggressor, Site, Aggression


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


def carge_municipio(data):
    """Municipio , Distrito, Región,  Código del municipio"""
    print(Region.objects.all().delete())
    municipios={}
    regiones = {}
    distritos = {}
    municipios_list = []
    municipios_dt = []
    for info in data:
        if info[2] in regiones:
            region = regiones[info[2]]
        else:
            region = Region.objects.create(name=info[2])
            regiones[info[2]] = region


        if info[1] in distritos:
            distrito = distritos[info[1]]
        else:
            distrito = District.objects.create(name=info[1], region=region)
            distritos[info[1]] = distrito

        if info[3] not in municipios_dt:
            municipios_list.append(Municipality(
                name=info[0],
                district=distrito,
                code = info[3],
                region=region
            ))
            municipios_dt.append(info[3])
    Municipality.objects.bulk_create(municipios_list)
    for muni in Municipality.objects.all():
        municipios[str(muni.code)] = muni
    return municipios

def calculate_speed(func, message, *args):
    """
    Calculate the time spend by a function call
    :param func:  Function to call
    :param message: Message to print when time speed is available
    :param args:  Arguments to pass to functions
    """
    start = time.time()
    dev = func(*args)
    end = time.time()
    print("Complete %s in "%message, end - start, " s")
    return dev

def carga_categoria(data):
    TypeAggression.objects.all().delete()
    dev = {}
    data_list=[]
    for dato in data:
        data_list.append( TypeAggression(name=dato))
    TypeAggression.objects.bulk_create(data_list)
    for obj in TypeAggression.objects.all():
        dev[obj.name] = obj
    return dev

def limpiar(value):
    dev = None
    value=value.strip().lower().replace(',  y ', "").replace('y', ',').strip(',').strip()
    if value:
        dev = value
    return value

def save_victim_site(victims, sites, municipios):
    Victim.objects.all().delete()
    Site.objects.all().delete()
    vic_list = []
    for victim in victims:
        vic_list.append(Victim(name=victim[0], age=victim[1] or None,
                          age_max=victim[2] or None, occupation=victim[3]))

    Victim.objects.bulk_create(vic_list)
    sites_list=[]
    for site in sites:
        sites_list.append(Site(name=site[0], municipality=municipios[ str(site[1])]))
    Site.objects.bulk_create(sites_list)
    return list(Victim.objects.all()), list(Site.objects.all())

def cargar_csv(request):
    total_start = time.time()
    if request.method == 'POST':
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            decoded_file = request.FILES['file'].read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=';', quotechar='"' )
            nueva_data = list(reader)
            nueva_data.pop(0)  # Quito los encabezados
            nueva_data.pop()
            nueva_data.pop()
            categorias= calculate_speed(carga_categoria, "Importa categorias" ,set(map(lambda x: x[0], nueva_data)))
            municipios = calculate_speed(carge_municipio, "Importa municipios", list(map(lambda x: x[16:20] , nueva_data)))
            agresiones = []
            victimas, sitios = calculate_speed(save_victim_site, "Guarda Víctimas",map(lambda x: x[4:8] , nueva_data),
                                                map(lambda x: (x[15],x[19]) , nueva_data),municipios)

            for i, data in enumerate(nueva_data):
                if i%100 ==0 :
                    start = time.time()
                victima = victimas[i]
                #Victim.objects.create(name=data[4], age=data[5] or None,
                #                               age_max=data[6] or None, occupation=data[7])
                if any(data[9:13]):
                    agresor = Aggressor.objects.create(
                        name=data[9],
                        age= limpiar(data[10]),
                        occupation = data[11] or "Desconocida",
                        victimRel = data[12] or None
                    )
                else:
                    agresor = None
                site = sitios[i]
                    #Site.objects.create(name=data[15], municipality=municipios[data[19]])
                agresiones.append(
                    Aggression(
                    name = victima.name,
                    victim = victima,
                    aggressors = agresor,
                    observations = data[22] or " ",
                    informer = data[21] or None,
                    source = data[1],
                    quantity = data[8],
                    detail = data[14] or None,
                    alleged_mobile =  data[20] or None,
                    aggression_type = categorias[data[0]],
                    sites =  site,
                    year = data[2] or 2020,
                    note_date =   datetime.strptime(data[3], '%d/%m/%Y').date() if data[3] else now()
                    ))
                if i % 100==0:
                    end = time.time()
                    print( "complete %d regs in" % i, end - start, " s")
            Aggression.objects.bulk_create(agresiones)

    else:
        form = CSVForm()

    total_end = time.time()
    print("Hecho en " , total_end - total_start, " s")
    context={'form': form, 'duracion': (total_end - total_start)/60, 'sduracion': total_end - total_start}
    return render(request, 'carga_csv.html', context=context)