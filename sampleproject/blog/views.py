from django.views.generic import ListView
from .models import BlogPost

class IndexView(ListView):
    
    template_name = 'index.html'
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hello'] = 'Hello World!'
        return context
        