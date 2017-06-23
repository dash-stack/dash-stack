import random, hashlib

from oslo_i18n import translate as _
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

from django.contrib.auth.models import User

from domain.models import Domain
from project.models import Project
from role.models import Assignment, Role
from .forms import UserRegisterForm
from user_profile.models import Profile
from sites.models import Sites


# email sending function
def send_email(con, subject, email_to, email_from):
    c = Context(con)
    text_content = render_to_string('mail/user_register_welcome.txt', c)
    html_content = render_to_string('mail/user_register_welcome.html', c)

    email = EmailMultiAlternatives(subject, text_content, email_from)
    email.attach_alternative(html_content, "text/html")
    email.to = [email_to]
    email.send()


def index(request):
    return render(request, "authcp/index.html", {})


# user registration
def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(
                form.cleaned_data['email'],
                form.cleaned_data['email'],
                form.cleaned_data['password2'],
            )
            u.is_active = False
            u.save()
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = form.cleaned_data['email']
            profile = Profile.objects.get(user_id=u.id)
            profile.activation_key = hashlib.sha1(salt + usernamesalt).hexdigest()
            profile.key_expires = timezone.now() + timedelta(days=2)
            # create domain ve new user
            domain = Domain.objects.create(
                name=form.cleaned_data['project'],
            )
            # create project for new user
            project = Project.objects.create(
                name=form.cleaned_data['project'],
                description='Project for %s ' % (u.username),
                domain=domain
            )
            # get role
            r = Role.objects.get(name="user")
            # assign new user as domain user
            assign_domain = Assignment.objects.create(
                type=3,
                actor=u,
                target_domain=domain,
                target_project=project,
                role=r
            )
            # assign new user as project user
            assign_project = Assignment.objects.create(
                type=1,
                actor=u,
                target_domain=domain,
                target_project=project,
                role=r,
            )
            # get first site
            site = Sites.objects.first()
            # get domain assignment
            domain = Assignment.objects.filter(actor=u.id)
            project = Assignment.objects.filter(actor=u.id)
            # if there is a site
            if site:
                # save site id to profile
                profile.selected_site = site.id
            profile.selected_domain = domain[0].target_domain_id
            profile.selected_project = project[0].target_project_id
            profile.save()
            # create domain for new user
            site_url = settings.SITE_ROOT_URL
            send_email({'u': u, 'profile': profile, 'site_url': site_url},
                       _('Welcome to our cloud'),
                       u.email,
                       settings.DEFAULT_EMAIL_FROM,
                       )
            return render(request,
                          'authcp/success.html',
                          {'u': u, 'profile': profile})
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'authcp/register.html', {'form': form})


# user registration success page
def register_success(request):
    return render(request, 'authcp/success.html', {})


# user activation
def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if timezone.now() > profile.key_expires:
            # Display: offer the user to send a new activation link
            activation_expired = True
            id_user = profile.user.id
        # Activation successful
        else:
            profile.user.is_active = True
            profile.user.save()
    # If user is already active, simply display error message
    else:
        # Display : error message
        already_active = True
    return render(request, 'authcp/activation.html', locals())
