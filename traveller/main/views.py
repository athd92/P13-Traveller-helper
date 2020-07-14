from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SearchForm
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserFormWithEmail, PostForm, ProfilForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import LoginView
from .geomap import GeoMaps
import pycountry
from main.models import Country, Post, Messages, UserAttributes
from django.http import JsonResponse
from datetime import date
from django.db.models import Count
from django.core.paginator import Paginator
from operator import itemgetter
import base64
from datetime import date, datetime
import os
import json


def index(request):
    """
    This function returns the  template
    """
    user = request.user
    month = datetime.now()
    month = month.strftime("%B")
    actual_month = month[0:3]

    mssg = Messages.objects.filter(author=user.id)
    choicelist = []
    c = Country.objects.all()
    for i in c:
        choicelist.append(i)

    post_count = Country.objects.annotate(Count("post"))

    clist = list(
        post_count.values_list(
            "name",
            "flag",
            "alpha_2",
            "post__count",
            "id",
            "resume",
            "picture",
            "temp_averges",            
        )
    )

    for i in range(0, len(clist)):
        clist[i] = list(clist[i])
        clist[i][-1] = json.dumps(eval(clist[i][-1]))

    clist = sorted(clist, key=itemgetter(3),)  # sort list by index[3] (posts)
    
    paginator = Paginator(clist, 6)  # Show  6  contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "actual_month": actual_month,
        "clist": clist,
        "choicelist": choicelist,
        "page_obj": page_obj,
        "mesages": mssg,
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
                    messages.success(request, "Logged in!")
                    return redirect("/")
                else:
                    return redirect('/')
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
                owner=user, avatar="", about="", img="", last_connexion=today
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
        messages.success(request, "Logged out!")
        return redirect("main:index")
    else:
        return redirect("main:index")


def account(request):
    if request.user.is_authenticated:
        img = UserAttributes.objects.filter(owner=request.user).latest(
            "id"
        )
        img = img.img
        infos = UserAttributes.objects.filter(owner=request.user).latest("id")
        name = request.user.username
        email = request.user.email
        context = {"name": name, "email": email, "img": img, "infos": infos}
        return render(request, "main/account.html", context)
    else:
        return redirect("/")


def posts(request):
    if request.method == "GET":
        country_id = request.GET.get("country_id")
        api_key = os.environ.get("FRONT_API_KEY")
        clist = []
        c = Country.objects.all()
        for i in c:
            clist.append(i)
        try:
            c = Country.objects.get(id=country_id)
        except ValueError:
            return redirect("/")
        except ObjectDoesNotExist:
            return redirect("/")
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
            "api_key": api_key,
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
                    budget=form.cleaned_data["budget"],
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
                mess = "Message sent!"
                context = {
                    "all_posts": all_posts,
                    "clist": clist,
                    "url": url,
                    "name": name,
                    "mess": mess,
                }
                messages.success(request, "Post sent!")
                return render(request, "main/posts.html", context)
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return render(request, "main/posts.html")


@requires_csrf_token
def delete_post(request) -> dict:
    if request.user.is_authenticated:
        try:
            post_id = request.POST["post_id"]
            selected_post = Post.objects.get(id=post_id)
            selected_post.delete()
            return JsonResponse({"result": "deleted"})
        except ValueError:
            return JsonResponse({"result": "failed"})
    else:
        return redirect("/")


@requires_csrf_token
def send_message(request) -> dict:
    """
    Function used to send message
    """
    if request.user.is_authenticated:        
        content = request.POST.get("message")
        author = request.user
        post_ref = request.POST.get("post_ref")
        post_id = Post.objects.get(id=post_ref)
        Messages.objects.create(
            title="", content=content, author=author, post_id=post_id
        )
        return JsonResponse({"message": "SEND OK"})
    return JsonResponse({"failed": "failed"})


@requires_csrf_token
def modify_post(request) -> dict:
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
    else:
        return redirect("/")


@requires_csrf_token
def upload_img(request) -> dict:
    """
    Function defined to upload profile image
    """
    if request.user.is_authenticated:
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
    else:
        return redirect("/")


def messages_posted(request):
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
    try:
        city = request.POST["city"]
        return JsonResponse({"result": "OK"})
    except MultiValueDictKeyError:
        return JsonResponse({"result": "failed"})


def update_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ProfilForm(request.POST)
            if form.is_valid():
                about = form.data.get("about")
                user = request.user
                user_atts = UserAttributes.objects.filter(owner=user).last()
                user_atts.about = about
                user_atts.save(update_fields=["about"])
                messages.success(request, "Profil updated")
                return redirect("/")
            else:
                messages.success(request, "Error while update")
                return redirect("/")
    else:
        return redirect("/")


@requires_csrf_token
def get_geocode(request):
    """
    Function defined to modify a specific post
    """

    country = request.POST["country"]
    city = request.POST["city"]
    coords = GeoMaps(country, city)
    coords = coords.get_geocode()
    context = {
        "coords": coords,
    }
    return JsonResponse(context)


def profil(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            username = request.GET.get("username")
            user = User.objects.get(username=username)
            infos = UserAttributes.objects.filter(owner=user).latest("id")
            context = {"infos": infos}
            return render(request, "main/profil.html", context)
        else:
            return render(request, "main/index.html")
    else:
        return redirect("/login")


def delete_message(request, message_id: int):
    if request.user.is_authenticated:
        mssg = Messages.objects.get(id=message_id)
        mssg.delete()
        user = request.user
        user_posts = Post.objects.filter(created_by=user.id)
        messages = Messages.objects.filter(post_id__in=user_posts)
        count = Messages.objects.filter(post_id__in=user_posts).count()
        context = {"messages": messages, "count": count}
        return render(request, "main/messages.html", context)
    else:
        return redirect('/')

    


