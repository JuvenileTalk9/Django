from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import BlogPost
from .forms import BlogPostForm

class IndexListView(ListView):
    
    template_name = 'index.html'
    model = BlogPost
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hello'] = 'Hello World!'
        return context


class IndexView(CreateView):
    
    template_name = 'index.html'
    form_class = BlogPostForm
    success_url = "/"
    