# /agent-django

Expert Django developer for web applications.

## Django Patterns
```python
# Model
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

# View (Class-based)
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/list.html'
    paginate_by = 20

# API View (DRF)
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

# Serializer
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at']
```

## Commands
```bash
python manage.py runserver
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
python manage.py test
python manage.py collectstatic
```
