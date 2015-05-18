import logging
import os
import sys
import ConfigParser
import re

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction

from ...models import *


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<ini file>'
    help = 'Import data from gnome-software.'

    def handle(self, *args, **options):

        # check arguments
        ini_file = '/usr/share/gnome-software/featured.ini'
        if len(args) == 1:
            ini_file = args[0]
        elif len(args) > 1:
            raise CommandError('Invalid number of arguments.\nType {} help importfeaturedapps'.format(
                os.path.basename(sys.argv[0])))

        logger.info('Reading %s' % ini_file)

        try:
            featured_config = ConfigParser.ConfigParser()
            featured_config.read([ini_file])
        except Exception as e:
            if settings.DEBUG:
                raise
            raise CommandError('Failed to read content of {ini_file}: {e}\nType {manage} help importfeaturedapps'.format(
                ini_file = ini_file, e = e, manage = os.path.basename(sys.argv[0])
                ))
        else:
            featured_apps_count = len(featured_config.sections())
            logger.info('Parsed {} featured apps'.format(featured_apps_count))


        # import featured apps
        errors = 0
        featured_app_ids = []
        for section in featured_config.sections():
            logger.info('Importing feature app {} ({}/{})'.format(
                section, len(featured_app_ids)+1, featured_apps_count,
            ))
            try:
                with transaction.atomic():
                    # find corresponding component
                    try:
                        c = Component.objects.get(type='desktop', type_id=section)
                    except Component.DoesNotExist:
                        logger.warn('Component desktop/{} does not exist!'.format(section))
                        featured_apps_count -= 1
                        continue

                    # create or update featured app
                    try:
                        fa = c.featured
                    except FeaturedApp.DoesNotExist:
                        fa = FeaturedApp(component=c)
                    fa.style = '; '.join(': '.join(item) for item in featured_config.items(section))
                    fa.style = re.sub(r'/usr/share/gnome-software/', "/static/images/", fa.style)
                    fa.style = re.sub(r'\stext:', " color:", fa.style)
                    fa.save()

            except Exception as e:
                logger.error('Failed to import node {}: {}'.format(section, e))
                if settings.DEBUG:
                    raise
                errors += 1
            else:
                featured_app_ids.append(fa.id)

        # check errors
        if errors > 0:
            raise CommandError('Failed to import featured apps: {} error(s)'.format(errors))
        else:
            logger.info('Successfully imported {} featured apps'.format(len(featured_app_ids)))

        # get stale featured apps
        stale_featured_apps = FeaturedApp.objects.exclude(id__in=featured_app_ids)
        stale_featured_apps_count = stale_featured_apps.count()

        # delete stale featured apps
        if stale_featured_apps_count > 0:
            stale_featured_apps.delete()
            logger.info('Successfully deleted {} stale featured apps'.format(stale_featured_apps_count))

