import os
import sys
from threading import Thread
from django.apps import AppConfig
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class TheAppConfig(AppConfig):
    name = 'the_app'

    def _run_script(self):

        channel_layer = get_channel_layer()

        print('sending')
        async_to_sync(channel_layer.group_send)('my-group', {
            'type': 'script.event',
            'message': 'Hello World!',
        })
        print('sent')

    def ready(self):
        if 'runserver' not in sys.argv or os.getenv('RUN_MAIN') != 'true':
            return

        thread = Thread(
            target=self._run_script,
            daemon=True,
        )
        thread.start()
