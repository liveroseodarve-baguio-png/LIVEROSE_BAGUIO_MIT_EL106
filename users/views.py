from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator


# 🧩 Registration UI with Email Verification
def register_ui(request):
    if request.method == 'POST':
        # username = request.POST['username']
        # email = request.POST['email']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # password = request.POST['password']
        # password2 = request.POST['password2']
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')


        # Validation
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register_ui')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register_ui')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_ui')

        # Create inactive user (must verify first)
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_active = False
        user.save()

        # Send verification email
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('verify_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email_message = EmailMessage(mail_subject, message, to=[email])
        email_message.send()

        messages.success(request, 'Registration successful! Please check your email to verify your account.')
        return redirect('login_ui')

    return render(request, 'register.html')


# 🧠 Account Activation View
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated! You can now log in.')
        return redirect('login_ui')
    else:
        return render(request, 'activation_invalid.html')


# 🔑 Login View
def login_ui(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, 'Please verify your email before logging in.')
                return redirect('login_ui')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login_ui')

    return render(request, 'login.html')


# 🏠 Dashboard View
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login_ui')
    return render(request, 'dashboard.html')


# 🚪 Logout View
def logout_ui(request):
    logout(request)
    return redirect('login_ui')
