from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .models import FeaturedApp, Component, Category


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        featured_app    = FeaturedApp.objects.order_by('?').first()
        highlight_apps  = Component.objects.filter(
            type='desktop',
            type_id__in=settings.FS_HIGHLIGHT_APPS,
        ).exclude(id=featured_app.component.id).order_by('?')[:12]
        highlight_cats = Category.objects.filter(
            slug__in=settings.FS_HIGHLIGHT_CATS,
        ).exclude(id=featured_app.component.id).order_by('?')[:12]
        return {
            'featured_app':     featured_app,
            'highlight_apps':   highlight_apps,
            'highlight_cats':   highlight_cats,
        }



class AppView(DetailView):
    model           = Component
    template_name   = 'app.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(
            type='desktop',
            type_id='{}.desktop'.format(self.kwargs['id']),
        )

    def get_context_object_name(self, obj):
        return 'app'



class CategoryView(DetailView):
    model           = Category
    template_name   = 'category.html'

class SearchView(TemplateView):
    template_name = 'search.html'

class FaqView(TemplateView):
    template_name = 'faq.html'
