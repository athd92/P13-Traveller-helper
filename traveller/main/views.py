from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SearchForm
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserFormWithEmail
from django.contrib.auth.views import LoginView


def index(request):
    """
    This function returns the  template
    """

    form = SearchForm(request.POST)
    context = {"form": form}

    return render(request, "main/index.html", context)


@requires_csrf_token
def get_infos(request):
    """
    Function used to send aliment infos by mail
    """
    if request.user.is_authenticated:
        if request.is_ajax():

            search = request.POST["search"]
            print("SEARCH")
            print(search)
            # aliment = Aliment.objects.get(id=aliment_id)
            # date = aliment.date
            # date = date[2:12]
            # email = request.user.email
            # email_from = settings.EMAIL_HOST_USER
            # subject = "Fiche aliment"
            # message = "Voici la fiche demandée"
            # subject, from_email, to = (
            #     "Fiche aliment Purbeurre",
            #     email_from,
            #     email_from,
            # )
            # try:
            #     text_content = "Une petite faim? Voici les informations demandées."
            #     context = {"aliment": aliment, "date": date}
            #     html_content = render_to_string("main/email_notif.html", context)
            #     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            #     msg.attach_alternative(html_content, "text/html")
            #     msg.send()
            #     return JsonResponse({"response": "ok"})
            # except:
            #     return JsonResponse({"response": "error"})
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
