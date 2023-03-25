from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class HomepageView(TemplateView):
    template_name = 'homepage.html'


def handler404(request, exception):
    return render(request, '404.html')
