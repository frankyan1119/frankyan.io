from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string


def home(request):
  return render(request, 'base/index.html')

def sendEmail(request):
  if request.method == 'POST':

    template = render_to_string('base/email_template.html', {
      'name': request.POST['name'],
      'email': request.POST['email'],
      'message': request.POST['message'],
    })

    email = EmailMessage(
      request.POST['subject'],
      template,
      settings.EMAIL_HOST_USER,
      ['yahao_yan@outlook.com']
    )

    email.send()

    return HttpResponse(status=204)