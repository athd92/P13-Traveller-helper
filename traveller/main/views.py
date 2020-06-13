from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SearchForm
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserFormWithEmail, PostForm
from django.contrib.auth.views import LoginView
import pycountry
from main.models import Country, Post, Messages, UserAttributes
from django.http import JsonResponse
from datetime import date
from django.db.models import Count
from django.core.paginator import Paginator
from operator import itemgetter
import base64
from datetime import date
import os


def index(request):
    """
    This function returns the  template
    """
    user = request.user
    messages = Messages.objects.filter(author=user.id)
    clist = []
    choicelist = []
    c = Country.objects.all()
    for i in c:
        choicelist.append(i)

    post_count = Country.objects.annotate(Count("post"))

    clist = list(
        post_count.values_list(
            "name", "flag", "alpha_2", "post__count", "id", "resume"
        )
    )  # list of tuple

    clist = sorted(clist, key=itemgetter(3),)  # sort list by index[3] (posts)
    clist.reverse()

    paginator = Paginator(clist, 6)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "clist": clist,
        "choicelist": choicelist,
        "page_obj": page_obj,
        "mesages": messages,
    }

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
            today = date.today()
            user_att = UserAttributes(
                owner=user,
                avatar="",
                about="",
                img="",
                last_connexion=today
            )
            user_att.save()

            return redirect("/")
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
        try:
            img = UserAttributes.objects.filter(owner=request.user).latest(
                "id"
            )
            img = img.img
        except ObjectDoesNotExist:
            img = ""
        name = request.user.username
        email = request.user.email
        context = {"name": name, "email": email, "img": img}
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
        name = c.name

        url = f"../static/img/flags/flag-{alpha}.jpg"
        user = request.user
        messages = Messages.objects.all()
        all_posts = Post.objects.filter(country__id=c.id)
        poster_pictures = {}
        for i in all_posts:
            user_instance = User.objects.get(username=i.created_by)
            try:
                user_attribut = UserAttributes.objects.filter(
                    owner=user_instance
                ).latest("id")
                poster_pictures[i.created_by] = user_attribut.img
            except:
                poster_pictures[i.created_by] = ""

        context = {
            "poster_pictures": poster_pictures,
            "messages": messages,
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
        form = PostForm(request.POST)

        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                country = Country.objects.get(
                    name=form.cleaned_data["country"]
                )

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


@requires_csrf_token
def delete_post(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                post_id = request.POST["post_id"]
                selected_post = Post.objects.get(id=post_id)
                selected_post.delete()
                return JsonResponse({"result": "deleted"})
            except EmptyResultSet:
                return JsonResponse({"result": "failed"})


@requires_csrf_token
def send_message(request):
    """
    Function used to send message
    """
    if request.user.is_authenticated:
        if request.is_ajax():
            content = request.POST["message"]
            author = request.user
            post_ref = request.POST.get("post_ref")
            post_id = Post.objects.get(id=post_ref)
            message = Messages.objects.create(
                content=content, author=author, post_id=post_id
            )

            return JsonResponse({"message": "SEND OK"})
    return JsonResponse({"failed": "failed"})


@requires_csrf_token
def modify_post(request):
    """
    Function defined to modify a specific post
    """
    if request.user.is_authenticated:
        if request.is_ajax():
            post_id = request.POST["post_id"]
            post = Post.objects.filter(id=post_id).values()
            post = post[0]

            context = {
                "post": post,
            }
            return JsonResponse(context)


@requires_csrf_token
def upload_img(request):
    """
    Function defined to upload profile image
    """
    if request.user.is_authenticated:
        if request.is_ajax():
            img64 = request.POST.get("img64")
            user = request.user
            today = date.today()
            new_img = UserAttributes.objects.create(
                owner=user,
                avatar="",
                last_connexion=today,
                about="",
                img=img64,
            )

            return JsonResponse({"ok": "ok"})


def messages(request):
    user = request.user
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(created_by=user.id)
        messages = Messages.objects.filter(post_id__in=user_posts)
        count = Messages.objects.filter(post_id__in=user_posts).count()
        context = {"messages": messages, "count": count}
        return render(request, "main/messages.html", context)
    else:
        return redirect("/")


@requires_csrf_token
def display_map(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                city = request.POST["city"]
                return JsonResponse({"result": "OK"})
            except ValueError:
                return JsonResponse({"result": "failed"})
