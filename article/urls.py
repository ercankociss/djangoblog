from django.contrib import admin
from django.urls import path
from . import views

app_name="article"

urlpatterns = [
    path('addarticle/', views.addarticle, name="addarticle"),
    path('delete/<int:id>', views.deletearticle, name="delete"),
    path('update/<int:id>', views.updatearticle, name="update"),
    path('articledetail/<int:id>', views.articledetail, name="detail"),
    path('addcomment/<int:id>', views.addcomment, name="addcomment"),
]

#Burada amac url'leri gruplamak ve ana url dosyasında yazılan metni kısaltmak
#Şİmdi bu grup article/create,article/delete, article/update şeklinde çağrılıyor olsun
#HEpsinde article/ ortak bu nedenle ana url dosyasında article/ yazılıp bu url include yapılacak bitecek