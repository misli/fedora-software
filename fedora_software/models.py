from django.db import models


class Origin(models.Model):
    origin  = models.CharField(max_length=100, unique=True)



class Category(models.Model):
    category    = models.CharField(max_length=100)



class CategoryName(models.Model):
    category    = models.ForeignKey(Category, related_name='names')
    lang        = models.CharField(max_length=100)
    name        = models.CharField(max_length=100)

    class Meta:
        unique_together = [('category', 'lang')]



class Keyword(models.Model):
    lang        = models.CharField(max_length=100, null=True)
    keyword     = models.CharField(max_length=100)



class Component(models.Model):
    origin      = models.ForeignKey(Origin, related_name='components')
    type        = models.CharField(max_length=100)
    type_id     = models.CharField(max_length=100)
    pkgname     = models.CharField(max_length=100)
    categories  = models.ManyToManyField(Category)
    keywords    = models.ManyToManyField(Keyword)
    project_license = models.TextField(null=True)



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

