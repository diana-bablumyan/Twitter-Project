from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserLoginForm, ProfileUpdateForm


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'users/register.html', context)


def user_login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('---')
    else:
        return render(request, 'users/user_login.html', {'form': form})


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request, user_id):
    if request.user.id != user_id:
        return HttpResponse("---")
    user_profile = Profile.objects.get(user_id=user_id)
    return render(request, "users/profile.html", {'profile': user_profile})

@login_required
def update_profile(request, profile_id):
    if request.user.profile.id != profile_id:
        return HttpResponse("---")

    profile = Profile.objects.get(id=profile_id)
    form = ProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        form = ProfileUpdateForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            # if request.FILES.get('profile_image', None) != None:
            #     profile.profile_image = request.FILES['profile_image']
            #     profile.save()
            return redirect('home')

    return render(request, "users/update_profile.html", {'form': form})
