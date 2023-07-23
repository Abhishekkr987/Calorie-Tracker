from django.shortcuts import render, redirect
from .models import Food,Consume
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                foods = Food.objects.all()
                consumed_food = Consume.objects.filter(user=request.user)
                return render(request, 'myapp/index.html', {'foods': foods, 'consumed_food': consumed_food})
            else:
                return HttpResponse("Invalid credentials, Please provide valid username and password !!!")
    else:
        form = LoginForm()
    return render(request,'myapp/login.html',{'form': form})



@login_required
def index(request):
    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user,food_consumed=consume)
        consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
    return render(request,'myapp/index.html',{'foods':foods,'consumed_food':consumed_food})


def delete_consume(request,id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request,'myapp/delete.html')