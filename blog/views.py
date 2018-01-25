from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Post
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from blog.forms import ContactForm

class ArticleListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('category') is not None:
            return Post.objects.filter(category=self.request.GET.get('category')).order_by('-published_date').all()
        return Post.objects.all().order_by('-published_date')


class ArticleDetailView(DetailView):
    model = Post


def contactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            print(subject, sender, message)
            # Если пользователь захотел получить копию себе, добавляем его в список получателей
            try:
                email = EmailMessage(subject, sender+'\n'+message, to=['indigogodman@gmail.com'])
                email.send()
            except BadHeaderError:  # Защита от уязвимости
                print('lol')
                return HttpResponse('Invalid header found')

            # Переходим на другую страницу, если сообщение отправлено
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
