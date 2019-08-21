from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from .forms import RegisterForm, LoginForm
from django.contrib.auth import logout
from django.utils.http import is_safe_url

User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        data = form.cleaned_data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        new_user = User.objects.create_user(username, email, password)
        if new_user is None:
            print("Create Error !")

    return render(request, "accounts/register.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.GET.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        data = form.cleaned_data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('home_url')
        else:
            print("Login error")

    return render(request, "accounts/login.html", context)


# def logout_url(request):
#     logout(request)
#     return redirect("accounts:login")