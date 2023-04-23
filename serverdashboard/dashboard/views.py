''' refer to Django documentation for details
(c) Franz Ludwig Kostelezky, <info@kostelezky.com>'''

from django.shortcuts import render, get_object_or_404
from .models import Server

def dashboard(request):
    ''' tba '''
    context = {
        'server_list': Server.objects.order_by('display_name')
    }

    return render(request, 'dashboard/dashboard.html', context)

def wake(request, server_id):
    ''' requires an valid id to a Server instance and sends a magic packet to it '''

    server = get_object_or_404(Server, id=server_id)
    server.wake_on_lan()

    context = {
        'server_list': Server.objects.order_by('display_name'),
        'message': {
            'type': 'success',
            'content': f'Magic packet to { server.display_name } was sent successfully!',
            }
    }

    return render(request, 'dashboard/dashboard.html', context)

def bitmap(request, server_id):
    ''' displaying the heuristic as bitmap
    '''
    server = get_object_or_404(Server, id=server_id)

    context = {
        'server': {
            'name': server.display_name,
            'ip_address': server.ip_address,
            },
        'bitmap': server.get_bitmap(),
    }

    return render(request, 'dashboard/bitmap.html', context)
