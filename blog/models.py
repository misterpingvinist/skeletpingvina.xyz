from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_text = RichTextUploadingField(blank=True, default='',max_length=300)
    text = RichTextUploadingField(blank=True, default='')
    category = models.ManyToManyField(Category)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    slug = models.CharField(max_length=100)
    image = models.ImageField(blank=True,null=True,default=None)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class About(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField()



from rest_framework import routers, serializers, viewsets

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title','pk')

class UserSerializer1(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    author = UserSerializer1(read_only=True, many=False)
    class Meta:
        model = Post
        fields = ('title','category','short_text','published_date','slug')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        username = self.request.query_params.get('category', None)
        if username is not None:
            return Post.objects.filter(category=username).order_by('-published_date').all()
        return Post.objects.order_by('-published_date').all()
