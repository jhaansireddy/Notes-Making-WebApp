from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from notesapp.models import Tag, Note
import datetime

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        x = request.user
        all_tags = Tag.objects.all()
        n = x.note_set.all()
        message =""
        if request.method=='POST':
            print(request.POST)
            l = request.POST.getlist('filter')
           # list = []
            for j in l:
                o = Tag.objects.get(id=int(j))
                bytag = o.note_set.all()
                n = bytag.intersection(n)
                print(n)
               # list.append(intersec)
            if 'search' in request.POST:
                searched = request.POST['search']
                n= n.filter(title__contains= searched).union(n.filter(content__contains= searched))
                if len(n) == 0:
                    message = "No results for '" + searched +"'"
        n=n.order_by('-createdon')
        nlist=[]
        for i in n:
            d={}
            d['title']=i.title
            d['date'] = i.createdon.strftime("%B") + " " + i.createdon.strftime("%d") + ", " + i.createdon.strftime("%Y") 
            d['id'] = i.id
            nlist.append(d)
        context = {'t':all_tags,
                    'nlist':nlist,
                    'message':message
                 }
        return render(request,'home2.html',context)
    else:
        return HttpResponseRedirect(reverse('ulogin'))

def ulogin(request):
    if request.method == 'POST':
        username = request.POST['usern']
        password = request.POST['passwd']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return HttpResponse("Please <a href='login'>register</a> first")
    return render(request,"userlogin.html")

def register(request):
    if request.method == 'POST':
        username = request.POST['email']
        p1 = request.POST['passwd1']
        p2 = request.POST['passwd2']
        a = User.objects.filter(username=username)
        if(len(a)>0):
            return HttpResponse("This is Email id already registered<br>Please, <a href='login'>SignIN</a>")
        elif p1 != p2:
            return HttpResponseRedirect(reverse('register'))
        else:
            user = User.objects.create_user(username,username,p1)
            user.save()
            return HttpResponseRedirect(reverse("ulogin"))
    
    return render(request,'register.html')

def ulogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ulogin'))

def addnote(request):
    if request.user.is_authenticated:
        x = request.user
        if request.method == 'POST':
            content = request.POST['content']
            title = request.POST['title']
            tags = request.POST.getlist('tags')
            n = Note.objects.create(title=title,content=content)
            n.save()
            n.user.add(x)
            for i in tags:
                y = Tag.objects.get(id=int(i))
                n.tags.add(y)
            return HttpResponseRedirect(reverse('home'))
        all_tags = Tag.objects.all()
        context = {'t':all_tags}
        return render(request,'addnote1.html',context)
    
    else:
        return HttpResponseRedirect(reverse('ulogin'))

def notedisplay(request,nid):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['action']=='0':
                Note.objects.filter(id=int(nid)).delete()
                return HttpResponseRedirect(reverse('home'))
            elif request.POST['action']=='1':
                return HttpResponseRedirect(reverse('editnote'))
        note = Note.objects.get(id=int(nid))
        tags = note.tags.all()
        all_tags = Tag.objects.all()
        date = note.createdon.strftime("%B") + " " + note.createdon.strftime("%d") + ", " + note.createdon.strftime("%Y") 
        context = {
            't':all_tags,
            'note':note,
            'date':date,
            'tags':tags
        }
        return render(request,'notedisplay.html',context)
    
    else:
        return HttpResponseRedirect(reverse('ulogin'))

def editnote(request,nid):
    if request.user.is_authenticated:
        x = request.user
        n = Note.objects.get(id=int(nid))
        if request.method == 'POST':
            content = request.POST['content']
            title = request.POST['title']
            tags = request.POST.getlist('tags')
            
            n.title = title
            n.content = content
            n.save()
            prevtags = n.tags.all()
            for i in prevtags:
                n.tags.remove(i)
            for i in tags:
                y = Tag.objects.get(id=int(i))
                n.tags.add(y)
            n.save()
            return HttpResponseRedirect(reverse('home'))
        all_tags = Tag.objects.all()
        title = n.title
        content = n.content 
        prevtags = n.tags.all()
        context = {'t':all_tags,
        'title':title,
        'content':content,
        'prevtags':prevtags}
        return render(request,'editnote.html',context)
    
    else:
        return HttpResponseRedirect(reverse('ulogin'))