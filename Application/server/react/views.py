from django.shortcuts import render
from django.views.generic import TemplateView

class PageView(TemplateView):
    '''
    Display initial react :template: 'react/index.html'.

    '''

    template_name = 'react/index.html'
