from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SearchForm
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserFormWithEmail
from django.contrib.auth.views import LoginView
import pycountry
from .country import Country
from django.http import JsonResponse


def index(request):
    """
    This function returns the  template
    """
    all_countries = list(pycountry.countries)
    clist = []
    for i in all_countries:
        clist.append(i.name)

    form = SearchForm(request.POST)
    context = {"form": form, "clist": clist}

    return render(request, "main/index.html", context)


@requires_csrf_token
def get_infos(request):
    """
    Function used to send aliment infos by mail
    """
    if request.is_ajax():

        search = request.POST["search"]
        search = search.capitalize()
        print(search)
        return JsonResponse({"search": search})

    return HttpResponse("Ajax sended")


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

            return redirect("main:homepage")
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
    all_countries = list(pycountry.countries)
    clist = []
    for i in all_countries:
        clist.append(i.name)

    form = SearchForm(request.POST)
    context = {"form": form, "clist": clist}

    return render(request, "main/posts.html", context)
