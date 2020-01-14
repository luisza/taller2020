from django.shortcuts import render
from django.utils.timezone import now

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