from django.contrib import admin
from .models import Article,Comment
# Register your models here.

#Bu şekilde register yeterli ancak admin modeli özelleştirmek için
#bu ifadeyi decorator olarak kullanıp, altta iç class ile Article modelini Admin modeline baglıyoruz
#admin.site.register(Article)

admin.site.register(Comment)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display=["title", "author","created_date"]
    list_display_links=["title", "created_date"]
    search_fields=["title"]
    list_filter=["created_date","title"]

    class Meta:
        model=Article

