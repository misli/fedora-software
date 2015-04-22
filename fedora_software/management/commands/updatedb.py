import gzip
import logging
import os
import sys

from datetime import datetime
from django.conf import settings
from django.core.management.base import CommandError
from django.utils.timezone import utc
from xml.etree import ElementTree

from . import LoggingBaseCommand
from ...models import *


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
                if settings.DEBUG:
                    raise
                raise CommandError(
                    'Failed to find xml file provided by appstream-data package. '\
                    'Specify path to the file as an argument.\nType {} help updatedb'.format(
                        os.path.basename(sys.argv[0])
                    ))
        elif len(args) > 1:
            raise CommandError('Invalid number of arguments.\nType {} help updatedb'.format(
                os.path.basename(sys.argv[0])))

        logger.info('Reading %s' % xml_file)

        try:
            tree = ElementTree.fromstring(gzip.open(xml_file,'rb').read())
        except Exception as e:
            if settings.DEBUG:
                raise
            raise CommandError('Failed to read content of {xml_file}: {e}\nType {manage} help updatedb'.format(
                xml_file = xml_file, e = e, manage = os.path.basename(sys.argv[0])
                ))

        try:
            o_origin = tree.attrib['origin']
        except:
            raise CommandError('Missing attribute components[origin]')
        origin = Origin.objects.get_or_create(origin=o_origin)[0]

        errors = 0
        component_ids = []
        for c_node in tree:
            c_type      = 'unknown'
            c_type_id   = 'unknown'

            try:
                c_type      = c_node.attrib['type']
                c_type_id   = c_node.find('id').text
                c_pkgname   = c_node.find('pkgname').text
                try:
                    c_project_license = c_node.find('project_license').text
                except:
                    c_project_license = None

                logger.info('Importing component {}/{}'.format(c_type, c_type_id))

                # create component
                c = Component.objects.get_or_create(
                    origin          = origin,
                    type            = c_type,
                    type_id         = c_type_id,
                    pkgname         = c_pkgname,
                    project_license = c_project_license,
                )[0]

                lang_attr = '{http://www.w3.org/XML/1998/namespace}lang'

                # create names
                c.names.all().delete()
                for c_name_node in c_node.findall('name'):
                    c.names.add(ComponentName(
                        lang = c_name_node.attrib.get(lang_attr),
                        name = c_name_node.text,
                    ))

                # create summaries
                c.summaries.all().delete()
                for c_summary_node in c_node.findall('summary'):
                    c.summaries.add(ComponentSummary(
                        lang = c_summary_node.attrib.get(lang_attr),
                        summary = c_summary_node.text,
                    ))

                # create descriptions
                c.descriptions.all().delete()
                for c_description_node in c_node.findall('description'):
                    c.descriptions.add(ComponentDescription(
                        lang = c_description_node.attrib.get(lang_attr),
                        description = c_description_node.text or '',
                    ))

                # create icons
                c.icons.all().delete()
                for c_icon_node in c_node.findall('icon'):
                    c.icons.add(ComponentIcon(
                        icon    = c_icon_node.text,
                        type    = c_icon_node.attrib.get('type'),
                        height  = c_icon_node.attrib.get('height'),
                        width   = c_icon_node.attrib.get('width'),
                    ))

                # create categories
                c.categories.all().delete()
                c_categories_node = c_node.find('categories')
                if c_categories_node is not None:
                    for category_node in c_categories_node.findall('category'):
                        c.categories.add(Category.objects.get_or_create(
                            category = category_node.text,
                        )[0])

                # create urls
                c.urls.all().delete()
                for c_url_node in c_node.findall('url'):
                    c.urls.add(ComponentUrl(
                        url     = c_url_node.text,
                        type    = c_url_node.attrib.get('type'),
                    ))

                # create screenshots
                c.screenshots.all().delete()
                c_screenshots_node = c_node.find('screenshots')
                if c_screenshots_node is not None:
                    for screenshot_node in c_screenshots_node.findall('screenshot'):
                        screenshot = ComponentScreenshot(
                            type = screenshot_node.attrib.get('type'),
                        )
                        c.screenshots.add(screenshot)
                        for image_node in screenshot_node.findall('image'):
                            screenshot.images.add(ComponentScreenshotImage(
                                image   = image_node.text,
                                type    = image_node.attrib.get('type'),
                                height  = image_node.attrib.get('height'),
                                width   = image_node.attrib.get('width'),
                            ))

                # create releases
                c.releases.all().delete()
                c_releases_node = c_node.find('releases')
                if c_releases_node is not None:
                    for release_node in c_releases_node.findall('release'):
                        c.releases.add(ComponentRelease(
                            version     = release_node.attrib.get('version'),
                            timestamp   = datetime.utcfromtimestamp(
                                int(release_node.attrib.get('timestamp'))
                            ).replace(tzinfo=utc)
                        ))

                # create languages
                c.languages.all().delete()
                c_languages_node = c_node.find('languages')
                if c_languages_node is not None:
                    for lang_node in c_languages_node.findall('lang'):
                        c.languages.add(ComponentLanguage(
                            percentage  = lang_node.attrib.get('percentage'),
                            lang        = lang_node.text,
                        ))

                # create metadata
                c.metadata.all().delete()
                c_metadata_node = c_node.find('metadata')
                if c_metadata_node is not None:
                    for value_node in c_metadata_node.findall('value'):
                        c.metadata.add(ComponentMetadata(
                            key     = value_node.attrib.get('key'),
                            value   = value_node.text,
                        ))

            except Exception as e:
                logger.error('Failed to import node {}/{}: {}'.format(c_type, c_type_id, e))
                if settings.DEBUG:
                    raise
                errors += 1
            else:
                component_ids.append(c.id)

        # check errors
        if errors > 0:
            raise CommandError('Failed to import components: {} error(s)'.format(errors))
        else:
            logger.info('Successfully imported {} components'.format(len(component_ids)))

        # get stale components
        stale_components = Component.objects.filter(origin=origin).exclude(id__in=component_ids)
        stale_components_count = stale_components.count()

        # delete stale components
        if stale_components_count > 0:
            stale_components.delete()
            logger.info('Successfully deleted {} stale components'.format(stale_components_count))

