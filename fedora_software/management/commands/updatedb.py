import logging
import os
import sys

from django.core.management.base import CommandError

from . import LoggingBaseCommand
from ...models import models


logger = logging.getLogger(__name__)


class Command(LoggingBaseCommand):
    args = '<xml file>'
    help = 'Import data from appstream-data. '

    def handle(self, *args, **options):
        self.configure_logging(options['verbosity'])

        # check arguments
        if len(args) == 1:
            xml_file = args[0]
        elif len(args) == 0:
            try:
                # try to find the file in rpm database
                import rpm
                header = rpm.TransactionSet().dbMatch('name', 'appstream-data').next()
                xml_file = filter(lambda f: f[0].endswith('.xml.gz'), header.fiFromHeader())[0][0]
            except:
                raise CommandError(
                    'Failed to find xml file provided by appstream-data package. '\
                    'Specify path to the file as an argument.\nType {} help updatedb'.format(
                        os.path.basename(sys.argv[0])
                    ))
        elif len(args) > 1:
            raise CommandError('Invalid number of arguments.\nType {} help updatedb'.format(
                os.path.basename(sys.argv[0])))

        logger.info('Reading %s' % xml_file)

