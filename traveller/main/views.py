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
from django.db.models import Count
from django.core.paginator import Paginator


def index(request):
    """
    This function returns the  template
    """
    clist = []
    choicelist = []
    c = Country.objects.all()
    for i in c:
        choicelist.append(i)

    post_count = Country.objects.annotate(Count("post"))
    clist = list(
        post_count.values_list("name", "flag", "alpha_2", "post__count")
    )  # list of tuple

    paginator = Paginator(clist, 6)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"clist": clist, "choicelist": choicelist, "page_obj": page_obj}

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
        print(country_id)
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
            posts = Post.objects.filter(country__id=c.id)
        except:
            posts = None

        all_posts = Post.objects.filter(country__id=c.id)
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
                country = Country.objects.get(
                    name=form.cleaned_data["country"]
                )
                print("COUNTRY")
                print(country.id)
                today = date.today()
                new_post = Post(
                    country=country,
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
                all_posts = Post.objects.filter(country__id=country.id)
                alpha = country.alpha_2
                url = f"../static/img/flags/flag-{alpha}.jpg"
                name = country.name
                context = {
                    "all_posts": all_posts,
                    "clist": clist,
                    "url": url,
                    "name": name,
                }
                return render(request, "main/posts.html", context)
            else:
                return HttpResponse(form.errors)

        else:
            return HttpResponse(form.non_field_errors)
    else:
        return render(request, "main/posts.html")
