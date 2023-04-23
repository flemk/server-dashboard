''' module models
(c) Franz Ludwig Kostelezky, <info@kostelezky.com>'''

import subprocess
import datetime
from django.db import models
from django.utils import timezone
from wakeonlan import send_magic_packet

class Timestamp(models.Model):
    ''' implements simple timestamp
    '''
    timestamp = models.DateTimeField()

    def happened_in_timeframe(self, delta_days, time_now):
        ''' returns true if timestamp is from last month, false otherwise'''
        return time_now - self.timestamp < datetime.timedelta(days=delta_days)

    def get_weekday(self):
        ''' returns weekday from 0=mon to 6=sun '''
        return self.timestamp.weekday()

class ServerActionTimeList(models.Model):
    ''' This is the heuristic when your server was woken
    '''

    list_of_timestamps = models.ManyToManyField(Timestamp, null=True, blank=True, default=None)

    def add_timestamp(self, timestamp):
        ''' creates new Timestamp instance from parameter timestamp and adds this to its list
        '''
        new_timestamp = Timestamp(timestamp=timestamp)
        new_timestamp.save()

        self.list_of_timestamps.add(new_timestamp)

    def count_actions(self, timestamp):
        ''' counts how often action was triggered in the past 30 days,
        on the same day in the same hour as param timestamp'''

        delta_days = 30

        timestamp_delta_days_ago = timezone.now() - datetime.timedelta(days=delta_days)
        weekday = timestamp.weekday()

        timestamps_in_hour_and_range = self.list_of_timestamps.filter(
            timestamp__hour=timestamp.hour,
            timestamp__gte=timestamp_delta_days_ago)

        timestamps_filtered = []
        for element in timestamps_in_hour_and_range.all():
            if element.get_weekday() != weekday:
                continue
            timestamps_filtered.append(element)

        return len(timestamps_filtered) / delta_days

class Server(models.Model):
    ''' implements a server model, having its properties as attributes
    '''
    display_name = models.CharField('Display-Name', max_length=20)
    ip_address = models.CharField('IP-Address', max_length=15)  # 255.255.255.255
    mac_address = models.CharField('MAC-Address', max_length=17)  # XX:XX:XX:XX:XX:XX

    endpoint_for_online_check = models.CharField('Online-check endpoint', max_length=30)
    endpoint_port_for_online_check = models.CharField('Online-check endpoint port', max_length=6)

    list_of_actions = models.ForeignKey(ServerActionTimeList,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        default=None,
                                        null=True)

    last_generated_bitmap = models.JSONField(blank=True, null=True, default=None)
    last_generated_bitmap_timestamp = models.DateTimeField(blank=True, null=True, default=None)

    def is_online(self):
        ''' pings the server on specified endpoint
        <endpoint_for_online_check>:<endpoint_port_for_online_check>
        returns <int: response_time> if successfull, false otherwise'''

        hostname = f'{ self.endpoint_for_online_check }:{ self.endpoint_port_for_online_check }'
        command = ["ping", "-c", "1", "-w2", hostname]

        return 'online' if subprocess.run(args=command,
                                          stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL,
                                          check=False).returncode == 0 else 'offline'

    def wake_on_lan(self):
        ''' sends the magic packet to <mac_address> and <ip_address>'''

        if self.list_of_actions is None:
            new_server_action_time_list = ServerActionTimeList()
            new_server_action_time_list.save()

            self.list_of_actions = new_server_action_time_list
            self.save()

        self.list_of_actions.add_timestamp(
            timestamp=timezone.now()
            )

        send_magic_packet(self.mac_address, ip_address=self.ip_address)

    def get_bitmap(self):
        ''' returns the WOL bitmap 
        returns previously stored bitmap if it was generated the past 24 hours
        generates and stores a new one else
        '''
        current_timestamp = timezone.now()
        current_weekday = current_timestamp.weekday() + 1
        current_hour = current_timestamp.hour

        if self.last_generated_bitmap is not None and \
            self.last_generated_bitmap_timestamp is not None:
            if self.last_generated_bitmap_timestamp \
                - current_timestamp <= datetime.timedelta(days=1):
                return self.last_generated_bitmap

        bitmap = {}
        for weekday in [0, 1, 2, 3, 4, 5, 6]:
            bitmap_hourly = {}
            for hour in range(24, 0, -1):
                timestamp = timezone.now() + \
                    datetime.timedelta(days=7 - current_weekday,
                                    hours=24 - current_hour) - \
                    datetime.timedelta(days=weekday, hours=hour)
                bitmap_hourly[timestamp.hour] = self.list_of_actions.count_actions(
                timestamp=timestamp)
            bitmap[timestamp.ctime()[:3]] = bitmap_hourly

        self.last_generated_bitmap = bitmap
        self.last_generated_bitmap_timestamp = current_timestamp
        self.save()

        return bitmap
