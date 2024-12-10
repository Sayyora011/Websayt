import requests
from django.conf import settings
from django.core.checks import translation
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from home.models import Settings, ContactMessage, ContactForm, SettingLang
from course.models import Course, Subject, Tutor, Student, SubjectLang, TutorLang
from django.contrib import messages

# Create your views here.
def index(request):
    # return HttpResponse("Hello Django")
    setting = Settings.objects.get()
    course = Course.objects.all()
    course_cr = Course.objects.all().order_by('id')[:4]
    subject_cr = Subject.objects.all().order_by('id')[:3]
    tutor_cr = Tutor.objects.all().order_by('id')[:3]
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    if defaultlang != currentlang:
        # setting = SettingLang.objects.get(lang=currentlang)
        subject_cr = SubjectLang.objects.filter(lang=currentlang).order_by('subject__id')
        # tutor_cr = TutorLang.objects.filter(tutorlang__lang=currentlang).order_by('id')
    page = "home"
    context = {'setting': setting,
               'page': page,
               'subject_cr': subject_cr,
               'course_cr': course_cr,
               'course': course,
               'tutor_cr': tutor_cr,}
    return render(request, 'index.html', context)

def about(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = Settings.objects.get()
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)
    context = {'setting': setting}
    # return HttpResponse("About us")
    return render(request, 'about.html', context)


TELEGRAM_BOT_TOKEN = ' 7418433765:AAFpXsNCBBD9pEN1NlFYdyFArx7Eapv-BNc '
TELEGRAM_CHANNEL = ' @hffyufvfu '
def contact(request):
    if request.method == 'POST':
        defaultlang = settings.LANGUAGE_CODE[0:2]
        currentlang = request.LANGUAGE_CODE[0:2]
        setting = Settings.objects.get()
        if defaultlang != currentlang:
            setting = SettingLang.objects.get(lang=currentlang)
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            phone = request.POST['phone']
            subject = request.POST['subject']
            message = request.POST['message']
            message_text = f'New message: \n\nName: {name} \nPhone: {phone} \nSubject: {subject} \nMessage: {message}'
            telegram_api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
            telegram_params = {'chat_id': {TELEGRAM_CHANNEL}, 'text': message_text}
            requests.post(telegram_api_url, params=telegram_params)
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.phone = form.cleaned_data['phone']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Thanks, " + data.name + "We received your message and will respond shortly...")
            return HttpResponseRedirect('/contact')
    setting = Settings.objects.get()
    context = {'setting': setting}
    # return HttpResponse("Contact page")
    return render(request, 'contact.html', context)



def tutors(request):
    tutor_cr = Tutor.objects.all().order_by('id')
    setting = Settings.objects.get()
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)
        tutor_cr = TutorLang.objects.filter(lang=currentlang)
    context = {'tutor_cr': tutor_cr,
               'setting': setting,}
    return render(request, 'tutors.html', context)

def students(request):
    student_cr = Student.objects.all().order_by('id')
    setting = Settings.objects.get()
    context = {'students_cr': student_cr,
               'setting': setting,}
    return render(request, 'students.html', context)

def subjects(request):
    subject_cr = Subject.objects.all().order_by('id')
    setting = Settings.objects.get()
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)
        subject_cr = SubjectLang.objects.filter(lang=currentlang).order_by('subject__id')
    setting = Settings.objects.get()
    context = {'subject_cr': subject_cr,
               'setting': setting,}
    return render(request, 'subjects.html', context)

def subject_detail(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    student_cr = Student.objects.all().order_by('id')
    setting = Settings.objects.get()
    if defaultlang != currentlang:
        try:
            prolang = SubjectLang.objects.get(subject=subjects, lang=currentlang)
            subjects.title = prolang.description
            subjects.keywords = prolang.keywords
            subjects.detail = prolang.detail
        except SubjectLang.DoesNotExist:
            pass
    context = {'students_cr': student_cr,
               'setting': setting,}
    return render(request, 'subject_detail.html', context)

def selectlanguage(request):
    if request.method == 'POST':

        lang = request.POST['language']
        # translation.active(lang)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang
        return HttpResponseRedirect("/" + lang)



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login

# Create your views here.
# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *


# Define a view function for the home page
def home(request):
    return render(request, 'home.html')


# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/home/')

    # Render the login page template (GET request)
    return render(request, 'login.html')


# Define a view function for the registration page
def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)

        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')

    # Render the registration page template (GET request)
    return render(request, 'register.html')






