from ..models import About
from blog.forms import ContactForm
from blog.models import Category


def about(request):
    about = About.objects.all()[0]
    category = Category.objects.all()
    form = ContactForm()
    return {
        'about_title': about.title,
        'about_text': about.text,
        'about_image': about.image.url,
        'category': category,
        'form_request':form
    }
