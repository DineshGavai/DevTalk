from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,UserRegister
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,"User does not exist !")
        
        user=authenticate(request,email=email,password=password) 
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Password does not match!")
            
    context={'page':page}
    return render(request,"Base/login_register.html",context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserRegister()
    if request.method == "POST":
        form=UserRegister(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred during registration")
    context={'form':form}
    return render(request,"Base/login_register.html",context)


def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''

    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        
        )
    topics=Topic.objects.all()[0:5]
    rooms_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))

    
    context={
        'rooms':rooms,
        'topics':topics,
        'rooms_count':rooms_count,
        'room_messages': room_messages
        }
    return render(request,'Base/home.html',context)


def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()    
    
    if request.method == "POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
            )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'Base/room.html',context)
    
    
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    room=user.room_set.all()
    topics=Topic.objects.all()
    room_messages=user.message_set.all()
    context={
        'user':user,
        'rooms':room,
        'topics':topics,
        'room_messages':room_messages
        }
    return render(request,'Base/profile.html',context)


@login_required(login_url='login')

def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            
        )
        return redirect('home')

    context={'form':form,'topics':topics}
    return render(request,"Base/room_form.html",context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse("Your not allowed to edit other's room!")
    
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('descriptiom')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(request,"base/room_form.html",context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Your not allowed to delete other's room!")
    
    if request.method=="POST":
        room.delete()
        return redirect("home")
    return render(request,"Base/delete.html",{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    
    if request.method=="POST":
        message.delete()
        return redirect("home")
    return render(request,"Base/delete.html",{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method == "POST":
        form=UserForm(request.POST,request.FILES , instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request,'Base/update-user.html',{'form':form})

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    # topics=Topic.objects.all()

    topics=Topic.objects.filter(
        Q(name__icontains=q) 
        
        )
    context={'topics':topics}
    return render(request,'Base/topics.html',context)

def activityPage(request):
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(request,'Base/activity.html',context)