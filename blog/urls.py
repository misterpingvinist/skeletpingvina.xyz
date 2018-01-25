from django.conf.urls import url, include

from blog.views import ArticleListView,ArticleDetailView,contactView
from blog.models import UserViewSet
from rest_framework import routers, serializers, viewsets


router = routers.DefaultRouter()
router.register(r'users', UserViewSet,base_name='posts')

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='article-list'),
    url(r'^api', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
    url(r'^contacts$', contactView),

]
