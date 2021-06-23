from django import forms
from .models import Article

#model olarak hazırladığımız article'dan form'u oluşturuyoruz
class ArticleForm(forms.ModelForm):
    
    class Meta :
        model= Article
        fields =["title", "content","article_image"]
