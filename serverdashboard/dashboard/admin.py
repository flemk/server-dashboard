''' refer to Django documentation for details
(c) Franz Ludwig Kostelezky, <info@kostelezky.com>'''

from django.contrib import admin
from django.utils import timezone
from .models import Server, ServerActionTimeList, Timestamp

class ServerAdmin(admin.ModelAdmin):
    '''custom view for class Server in admin interface'''
    list_display = ('display_name',
                    'ip_address',
                    'mac_address',
                    'endpoint_for_online_check',
                    'endpoint_port_for_online_check',)
admin.site.register(Server, ServerAdmin)

class ServerActionTimeListAdmin(admin.ModelAdmin):
    '''custom view for class Server in admin interface'''
    list_display = ('id', 'fetch_count_actions', )

    def fetch_list_of_timestamps(self, instance):
        ''' returns instance.list_of_timestamps as string
        '''
        return str(instance.list_of_timestamps.all())

    def fetch_count_actions(self, instance):
        ''' returns instance.count_actions as string
        '''
        return str(instance.count_actions(timestamp=timezone.now()))
admin.site.register(ServerActionTimeList, ServerActionTimeListAdmin)

class TimestampAdmin(admin.ModelAdmin):
    '''custom view for class Timestamp in admin interface'''
    list_display = ('id', 'timestamp', 'fetch_happened_in_timeframe', 'fetch_weekday')

    def fetch_weekday(self, instance):
        ''' returns instance.timestamp.weekday as string
        '''
        return instance.timestamp.weekday()

    def fetch_happened_in_timeframe(self, instance):
        ''' returns instance.happened_in_timeframe as string
        '''
        return instance.happened_in_timeframe(delta_days=30, time_now=timezone.now())
admin.site.register(Timestamp, TimestampAdmin)
