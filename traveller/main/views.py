from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SearchForm
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserFormWithEmail, PostForm
from django.contrib.auth.views import LoginView
import pycountry
from .models import Country, Post
from django.http import JsonResponse
from datetime import date


def index(request):
    """
    This function returns the  template
    """
    clist = []
    c = Country.objects.all()
    for i in c:
        clist.append(i)
    context = {"clist": clist}

    return render(request, "main/index.html", context)


def login_request(request):
    """
    This functions is used to get the user logged if
    the Auth is auth is success
    """
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
                else:
                    pass
            else:
                pass
        form = AuthenticationForm()
        return render(
            request=request,
            template_name="main/login.html",
            context={"form": form},
        )


def register(request):
    """
    This function returns the register form template
    """
    if request.method == "POST":
        form = UserFormWithEmail(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            login(request, user)

            return render(request, "main/index.html")
        else:
            return render(
                request=request,
                template_name="main/register.html",
                context={"form": form},
            )

    form = UserFormWithEmail
    return render(
        request=request,
        template_name="main/register.html",
        context={"form": form},
    )


def logout_request(request):
    """
    This function is used by the user to logout
    """
    if request.user.is_authenticated:
        logout(request)
        return redirect("main:index")
    else:
        return redirect("main:index")


def account(request):
    if request.user.is_authenticated:
        name = request.user.username
        email = request.user.email
        context = {"name": name, "email": email}
        return render(request, "main/account.html", context)
    else:
        return redirect("/")


def posts(request):
    if request.method == "GET":
        country_id = request.GET.get("country_id")
        clist = []
        c = Country.objects.all()
        for i in c:
            clist.append(i)
        c = Country.objects.get(id=country_id)
        alpha = c.alpha_2
        print(alpha)
        name = c.name

        url = f"../static/img/flags/flag-{alpha}.jpg"
        user = request.user
        try:
            posts = Post.objects.filter(country=c.name)
        except:
            posts = None

        all_posts = Post.objects.filter(country=c.name)
        context = {
            "url": url,
            "user": user,
            "form": "form",
            "clist": clist,
            "name": name,
            "country_id": country_id,
            "all_posts": all_posts,
        }

    return render(request, f"main/posts.html", context)


def send_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                today = date.today()
                new_post = Post(
                    country=form.cleaned_data["country"],
                    city=form.cleaned_data["city"],
                    total_travelers=form.cleaned_data["total"],
                    wanted_travelers=form.cleaned_data["wanted"],
                    free_places=form.cleaned_data["free"],
                    interest=form.cleaned_data["interest"],
                    title=form.cleaned_data["title"],
                    message=form.cleaned_data["message"],
                    start_date=form.cleaned_data["start"],
                    end_date=form.cleaned_data["end"],
                    ready=False,
                    created_by=request.user,
                )
                new_post.save()
                clist = []
                c = Country.objects.all()
                for i in c:
                    clist.append(i)
                all_posts = Post.objects.filter(
                    country=form.cleaned_data["country"]
                )
                context = {"all_posts": all_posts, "clist": clist}
                return render(request, "main/posts.html", context)
            else:
                return HttpResponse(form.errors)

        else:
            return HttpResponse(form.non_field_errors)
    else:
        return render(request, "main/posts.html")