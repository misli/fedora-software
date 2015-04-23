from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .models import FeaturedApp, Component


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        return {
            'featured_app': FeaturedApp.objects.order_by('?').first(),
        }



class AppView(DetailView):
    model = Component
    template_name = 'app.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(
            type='desktop',
            type_id='{}.desktop'.format(self.kwargs['id']),
        )

    def get_context_object_name(self, obj):
        return 'app'



class SearchView(TemplateView):
    template_name = 'search.html'

class CategoryView(TemplateView):
    template_name = 'category.html'

class FaqView(TemplateView):
    template_name = 'faq.html'
