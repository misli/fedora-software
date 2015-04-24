from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import get_language


class Category(models.Model):
    slug        = models.CharField(max_length=100, unique=True)
    category    = models.CharField(max_length=100, unique=True)

    def get_name(self):
        try:
            return self.names.get(lang=get_language()).name
        except CategoryName.DoesNotExist:
            try:
                return self.names.get(lang=None).name
            except CategoryName.DoesNotExist:
                return self.category

    def get_absolute_url(self):
        return reverse('category', args=(self.slug,))

    @property
    def addons(self):
        return self.components.filter(type='addon')

    @property
    def codecs(self):
        return self.components.filter(type='codec')

    @property
    def desktops(self):
        return self.components.filter(type='desktop')

    @property
    def fonts(self):
        return self.components.filter(type='font')

    @property
    def inputmethods(self):
        return self.components.filter(type='inputmethod')

    @property
    def webapps(self):
        return self.components.filter(type='webapp')


class CategoryName(models.Model):
    category    = models.ForeignKey(Category, related_name='names')
    lang        = models.CharField(max_length=100, null=True)
    name        = models.CharField(max_length=100)

    class Meta:
        unique_together = [('category', 'lang')]



class Keyword(models.Model):
    lang        = models.CharField(max_length=100, null=True)
    keyword     = models.CharField(max_length=100)



class Component(models.Model):
    type        = models.CharField(max_length=100)
    type_id     = models.CharField(max_length=100)
    pkgname     = models.CharField(max_length=100)
    categories  = models.ManyToManyField(Category, related_name='components')
    keywords    = models.ManyToManyField(Keyword)
    project_license = models.TextField(null=True)

    class Meta:
        unique_together = [('type', 'type_id')]

    def get_name(self):
        try:
            return self.names.get(lang=get_language()).name
        except ComponentName.DoesNotExist:
            try:
                return self.names.get(lang=None).name
            except ComponentName.DoesNotExist:
                return self.pkgname

    def get_summary(self):
        try:
            return self.summaries.get(lang=get_language()).summary
        except ComponentSummary.DoesNotExist:
            try:
                return self.summaries.get(lang=None).summary
            except ComponentSummary.DoesNotExist:
                return ''

    def get_description(self):
        try:
            return self.descriptions.get(lang=get_language()).description
        except ComponentDescription.DoesNotExist:
            try:
                return self.descriptions.get(lang=None).description
            except ComponentDescription.DoesNotExist:
                return ''

    def get_absolute_url(self):
        if self.type == 'desktop':
            return reverse('app', args=(self.type_id[:-8],))
        else:
            raise Exception('not implemented url: {}'.format(self.type))

    def get_icon_url(self):
        try:
            return self.icons.first().icon
        except ComponentIcon.DoesNotExist:
            return ''
    def get_version(self):
        try:
            return self.releases.first().version;
        except ComponentRelease.DoesNotExist:
            return ''




class ComponentName(models.Model):
    component   = models.ForeignKey(Component, related_name='names')
    lang        = models.CharField(max_length=100, null=True)
    name        = models.CharField(max_length=100)

    class Meta:
        unique_together = [('component', 'lang')]



class ComponentSummary(models.Model):
    component   = models.ForeignKey(Component, related_name='summaries')
    lang        = models.CharField(max_length=100, null=True)
    summary     = models.TextField()

    class Meta:
        unique_together = [('component', 'lang')]



class ComponentDescription(models.Model):
    component   = models.ForeignKey(Component, related_name='descriptions')
    lang        = models.CharField(max_length=100, null=True)
    description = models.TextField()

    class Meta:
        unique_together = [('component', 'lang')]



class ComponentIcon(models.Model):
    component   = models.ForeignKey(Component, related_name='icons')
    type        = models.CharField(max_length=100)
    icon        = models.CharField(max_length=100)
    height      = models.IntegerField(null=True)
    width       = models.IntegerField(null=True)



class ComponentUrl(models.Model):
    component   = models.ForeignKey(Component, related_name='urls')
    type        = models.CharField(max_length=100)
    url         = models.CharField(max_length=100)



class ComponentScreenshot(models.Model):
    component   = models.ForeignKey(Component, related_name='screenshots')
    type        = models.CharField(max_length=100, null=True)

    def get_small_thumbnail_image(self):
        try:
            return self.images.get(type='thumbnail',
                height=settings.FS_SMALL_THUMBNAIL_HEIGHT,
                width=settings.FS_SMALL_THUMBNAIL_WIDTH)
        except ComponentScreenshotImage.DoesNotExist:
            return None

    def get_medium_thumbnail_image(self):
        try:
            return self.images.get(type='thumbnail',
                height=settings.FS_MEDIUM_THUMBNAIL_HEIGHT,
                width=settings.FS_MEDIUM_THUMBNAIL_WIDTH)
        except ComponentScreenshotImage.DoesNotExist:
            return None

    def get_large_thumbnail_image(self):
        try:
            return self.images.get(type='thumbnail',
                height=settings.FS_LARGE_THUMBNAIL_HEIGHT,
                width=settings.FS_LARGE_THUMBNAIL_WIDTH)
        except ComponentScreenshotImage.DoesNotExist:
            return None

    def get_source_image(self):
        try:
            return self.images.get(type='source')
        except ComponentScreenshotImage.DoesNotExist:
            return None



class ComponentScreenshotImage(models.Model):
    screenshot  = models.ForeignKey(ComponentScreenshot, related_name='images')
    type        = models.CharField(max_length=100, null=True)
    height      = models.IntegerField(null=True)
    width       = models.IntegerField(null=True)
    image       = models.CharField(max_length=1000)



class ComponentRelease(models.Model):
    component   = models.ForeignKey(Component, related_name='releases')
    version     = models.CharField(max_length=100)
    timestamp   = models.DateTimeField()



class ComponentLanguage(models.Model):
    component   = models.ForeignKey(Component, related_name='languages')
    percentage  = models.IntegerField(null=True)
    lang        = models.CharField(max_length=100)



class ComponentMetadata(models.Model):
    component   = models.ForeignKey(Component, related_name='metadata')
    key         = models.CharField(max_length=100)
    value       = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = [('component', 'key')]



class FeaturedApp(models.Model):
    component   = models.OneToOneField(Component, related_name='featured')
    style       = models.TextField()

