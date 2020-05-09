from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchForm
from django.views.decorators.csrf import requires_csrf_token


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
    return HttpResponse('Ajax sended')
