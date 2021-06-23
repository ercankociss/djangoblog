from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Article(models.Model):
    #verbose_name kullanılmazsa django değişkenlere göre isim verir
    author=models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Yazar")
    title=models.CharField(max_length=50, verbose_name="Başlık")
    content = RichTextField()
    created_date= models.DateTimeField(auto_now_add=True)
    article_image=models.FileField(blank=True, null=True, verbose_name="Makaleye Foto Ekleyin")
    #article'nın isminin istenilen  şekilde görülmesi
    def __str__(self):
        return self.title


class Comment(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE, verbose_name="Makale", related_name="comments_related")
    comment_author=models.CharField(max_length=50, verbose_name="Yorumcu")
    comment_content=models.CharField(max_length=200, verbose_name="Yorumİçerik")
    comment_date=models.DateTimeField(auto_now_add=True)
    ''' def __str__(self):
        return self.comment_content '''