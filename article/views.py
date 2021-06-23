from django.shortcuts import render, redirect, HttpResponse,get_object_or_404,reverse
from .forms import ArticleForm 
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Article,Comment
from django.contrib.auth.decorators import login_required

# Create your views here.

#view'e yazılan fonk.lara mutlaka ilk arguman olarak request mutlaka yazılmallı
def index (request):
    #bu sekilde direk bir Httpresponse donebilir.
    #return HttpResponse("<h3>Ana Sayfa view'den</h3>")
    
    #templates kalsorunun altın da ise boyle degilse or.: article/index.html seklinde belirtilmeli
    
    return render (request, "index.html")

def about(request):

    return render(request, "about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    keyword=request.GET.get("keyword")
    if keyword:
        articlelist=Article.objects.filter(title__contains=keyword)
        userarticlelist=Article.objects.filter(author=request.user,title__contains=keyword)
    else:
        articlelist=Article.objects.all()
        userarticlelist=Article.objects.filter(author=request.user)
    return render(request, "dashboard.html", {"articlelist":articlelist, "userarticlelist":userarticlelist})

def articles(request):
    keyword=request.GET.get("keyword")
    if keyword:
        articlelist=Article.objects.filter(title__contains=keyword)
    else:
        articlelist=Article.objects.all()
    return render(request, "articles.html", {"articlelist":articlelist})

def articledetail(request, id):
    article=Article.objects.get(id=id)
    comments=Comment.objects.filter(article_id=id)
    return render(request,"articledetail.html",{"article":article, "comments":comments} )

#bu benim yazdığım, login_required eklenince artık giriş yapılma kontrolunun yapılmasına gerek kalmayacak yenisi altta 
def addarticleerc(request):
    form=ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        if request.user.is_authenticated:
            #newarticle=form.save(commit=False)
            newarticle=Article(title=form.cleaned_data.get("title"), content=form.cleaned_data.get("content"),author=request.user)
            ''' newarticle.title=form.cleaned_data.get("title")
            newarticle.content=form.cleaned_data.get("content")
            newarticle.author=request.user '''
            if request.FILES:
                newarticle.article_image=request.FILES["article_image"]
            newarticle.save()
            messages.success(request, "Makale Başarılı şekilde kaydedildi")
            return render(request, "addarticle.html", {"form":form})
        else: 
            messages.warning(request, "Öncelikle giriş yapmalısınız")
            return redirect("/./user/login")
    return render(request, "addarticle.html", {"form":form})    

@login_required(login_url="user:login")
def addarticle(request):
    form=ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        newarticle=form.save(commit=False)
        newarticle.author=request.user
        if request.FILES:
            newarticle.article_image=request.FILES["article_image"]
        newarticle.save()
        messages.success(request, "Makale Başarılı şekilde kaydedildi")
    return render(request, "addarticle.html", {"form":form})    


def updatearticle(request, id):
    articletoupdate=get_object_or_404(Article, id=id)
    form=ArticleForm(request.POST or None, request.FILES or None, instance=articletoupdate)
    if form.is_valid():
        articletoupdate=form.save(commit=False)
        articletoupdate.author=request.user
        articletoupdate.save()
        messages.info(request, articletoupdate.title+" isimli makale güncellendi")
        
    return render(request, "updatearticle.html", {"form":form,"id":id, "image":articletoupdate.article_image})


#Acemi işi ben kendim yazmıştım oysa pratik olanı ustte
def updatearticleerc(request,id):
    form=ArticleForm(request.POST or None, request.FILES or None)
    articletoupdatespec=Article.objects.get(id=id)
    #Bu şekilde bulunmayan bir article çağrılırsa hata 404 sayfasını getirecektir.
    articletoupdate=get_object_or_404(Article, id=id)
    if form.is_valid():
        if request.user.is_authenticated:
            if request.user==articletoupdate.author:
                articletoupdate.title=form.cleaned_data.get("title")
                articletoupdate.content=form.cleaned_data.get("content")
                if request.FILES:
                    articletoupdate.article_image=request.FILES["article_image"]
                articletoupdate.save()
                messages.info(request, articletoupdate.title+" isimli makale güncellendi")
                return render(request, "updatearticle.html", {"form":form,"id":id,"article":articletoupdate})
            else :
                messages.warning(request, "Sadece kendi makalelerinizi güncelleyebilirsiniz")
                return redirect ("dashboard")
        else :
            messages.warning(request, "Öncelikle giriş yapmalısınız")
            return redirect("/./user/login")
    else:
        form=ArticleForm({
            "title":articletoupdate.title,
            "content":articletoupdate.content
        })
        return render(request, "updatearticle.html", {"form":form,"id":id})


def deletearticle(request,id):
    #articletodelete=Article.objects.get(id=id)
    articletodelete=get_object_or_404(Article, id=id)   
    if request.user.is_authenticated:
        if request.user==articletodelete.author:
           articletodelete.delete()
           messages.info(request, articletodelete.title+" isimli makale silindi")
           return redirect ("dashboard")
        else :
            messages.warning(request, "Sadece kendi makalelerinizi silebilirsiniz")
            #eger url ana url sayfası haricinde bir yerde ise örnek article altinda olsun
            #o zaman ("article:dashboard") şeklinde belirtilir.
            return redirect ("dashboard")
    else :
        messages.warning(request, "Öncelikle giriş yapmalısınız")
        return redirect("/./user/login")

def addcomment(request, id):
    newComment=Comment(comment_author=request.POST.get("comment_author"), comment_content=request.POST.get("comment_content"), article_id=id)
    newComment.save()
         #Bu reverse kullanımı dinamik url kullanımına imkan veriyor
        #return redirect("article/detail"+id) şeklinde olabilirdi ancak alttaki kullanımı önemli
    messages.success(request, "Yorumunuz başarılı şekilde kaydedildi") 
    #return render(request, "articledetail.html", {"id":id})
    return redirect(reverse("article:detail",kwargs={"id":id,}))

""" class Comments-UserMapDataFrame(models.Model):
    user = models.ForeignKey(User-Article) 
    User.usermapdataframe_set.all()
    Article.comments_set.all()
 """

def showcomments(request):
    commentlist=Comment.objects.filter(article_id=19)
    #commentlist=commentlist.filter(article_id=18)
    #commentlist=(commentlist)
    # length=len(commentlist)
    # first=commentlist[0]

    return render (request,"showcomments.html", {"comments":commentlist}) 