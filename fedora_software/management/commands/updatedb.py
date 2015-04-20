import logging
import os

from optparse import make_option

from django.core.management.base import CommandError

from multiprocessing import Pool, cpu_count

from . import LoggingBaseCommand
from ...models import models


logger = logging.getLogger(__name__)


class Command(LoggingBaseCommand):
    help = 'Import data from appstream-data.'

    def handle(self, *args, **options):
        self.configure_logging(options['verbosity'])
        errors = 0
        self.stdout.write('It works!')

