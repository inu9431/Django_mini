import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'Wait for db to be available'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for db...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS('db available'))
                break
            except OperationalError:
                self.stdout.write(('db unavailable, waiting 1 second ...'))
                time.sleep(1)

