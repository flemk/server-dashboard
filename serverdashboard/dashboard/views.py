''' refer to Django documentation for details
(c) Franz Ludwig Kostelezky, <info@kostelezky.com>'''

import datetime
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Server

def dashboard(request):
    ''' tba '''
    context = {
        'server_list': Server.objects.order_by('display_name')
    }

    return render(request, 'dashboard/dashboard.html', context)

def wake(request, id):
    ''' requires an valid id to a Server instance and sends a magic packet to it '''

    server = get_object_or_404(Server, id=id)
    server.wake_on_lan()

    context = {
        'server_list': Server.objects.order_by('display_name'),
        'message': {
            'type': 'success',
            'content': f'Magic packet to { server.display_name } was sent successfully!',
            }
    }

    return render(request, 'dashboard/dashboard.html', context)

def bitmap(request, id):
    '''
    '''
    server = get_object_or_404(Server, id=id)

    context = {
        'bitmap': server.get_bitmap(),
    }

    return render(request, 'dashboard/bitmap.html', context)
