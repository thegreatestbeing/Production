from django.conf                import settings
from django.core.mail           import send_mail
from datetime                   import timedelta
from django.contrib             import messages
from django.contrib.auth        import login, logout
from django.contrib.auth        import get_user_model
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.auth.forms  import AuthenticationForm
from django.urls                import reverse, reverse_lazy
from django.http                import HttpResponse
from django.views.generic       import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit  import FormMixin
from django.shortcuts           import render, redirect, get_object_or_404
from django.views               import (
    View,
    generic
    )
from django.views.generic.detail import DetailView
from django.template.loader     import get_template
from django.utils               import timezone
from django.utils.http          import is_safe_url
from django.utils.safestring    import mark_safe

from django.contrib.auth        import authenticate

# from APIs.models import Follow

from Business.mixins    import NextUrlMixin, RequestFormAttachMixin
from Business.utils     import GenerateOTP, random_string_generator, unique_key_generator
from Account.forms      import SignupForm, LoginForm, OTPForm, ReactivateEmailForm
from Account.models     import EmailActivation

from .models            import Profile



class EmailActivate(FormMixin, View):
    success_url = '/'
    form_class 	= ReactivateEmailForm
    link 		= None
    def get(self, request, link=None, *args, **kwargs):
        self.link = link
        if link is not None:
            qs = EmailActivation.objects.filter(link__iexact=link)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
        context = {'form': self.get_form(),'link': link}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg                 = """Activation link sent, please check your email."""
        request             = self.request
        messages.success(request, msg)

        email               = form.cleaned_data.get("email")
        obj                 = EmailActivation.objects.email_exists(email).first()
        valid_till          = timezone.now() + timedelta(minutes=4)
        obj_instance        = EmailActivation.objects.get(email=email)
        obj_instance.email  = email
        obj_instance.valid  = valid_till        
        obj_instance.save()
        obj_instance.send_activation()
        # obj_instance.send_opt()
        return super(EmailActivate, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "link": self.link }
        return render(self.request, 'registration/activation-error.html', context)


def DeleteAccount(request):
	pass


def DisableAccount(request):
	pass


def OTPActivate(request):
	if request.user.is_authenticated:
		key 	= ''
		active  = ''
		name 	= request.user.first_name
		user 	= request.user.username
		profile = ''
		expired = ''


		for i in Profile.objects.filter(user=request.user):
			profile = i.profile_pic
		for i in EmailActivation.objects.filter(user=request.user):
			key 	= int(i.OTP)
			active 	= i.activated

			if timezone.now() <= i.valid:
				expired = False
			else : 
				expired = True
		if request.method == 'POST':
			otp_form  	= OTPForm(request.POST)
			if otp_form.is_valid():
				otp 	= request.POST.get('OTP')
				# print(otp)
				if int(otp) == key and not active and not expired:
					activate = EmailActivation.objects.get(user=request.user)
					activate.activated  = True
					activate.save()
					activate.send_activation()
					return redirect("/")
		else:
			otp_form 	= OTPForm()

	return render(request, 'account/otp.html', {
			'otp_form' : otp_form,
		})


# def ResendOTP(request):
#     if request.user.is_authenticated:
#         key     = ''
#         active  = ''
#         name    = request.user.first_name
#         user    = request.user.username
#         profile = ''
#         expired = ''


#         for i in Profile.objects.filter(user=request.user):
#             profile = i.profile_pic
#         for i in EmailActivation.objects.filter(user=request.user):
#             key     = int(i.OTP)
#             active  = i.activated

#             if timezone.now() <= i.valid:
#                 expired = False
#             else : 
#                 expired = True
#         if request.method == 'POST':
#             otp_form    = OTPForm(request.POST)
#             if otp_form.is_valid():
#                 otp     = request.POST.get('OTP')
#                 print(otp)
#                 if int(otp) == key and not active and not expired:
#                     activate = EmailActivation.objects.get(user=request.user)
#                     activate.activated  = True
#                     activate.save()
#                     return redirect("/")
#         else:
#             otp_form    = OTPForm()

#     return render(request, 'account/otp.html', {
#             'otp_form' : otp_form,
#         })


# class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
#     form_class = LoginForm
#     success_url = '/'
#     template_name = 'account/login.html'
#     default_next = '/'

#     def form_valid(self, form):
#         next_path = self.get_next_url()
#         return redirect(next_path)


# def Login(request):
#     login   = AuthenticationForm()

#     if request.method == 'POST':
#         login   = LoginForm(request.POST or None)

#         print('trying to login')

#         if login.is_valid():
#             # username    = login.cleaned_data.get("username")
#             # password    = login.cleaned_data.get("password")

#             # user        = authenticate(request, username=username, password=password)

#             return redirect('/')

#     return render(request, 'account/login.html', {
#         'login'    : login
#     })



def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__

        username    = request.POST['username']
        password    = request.POST['password']
        user        = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('/')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'account/login.html', {'form':form, 'title':'log in'})


def Logout(request):
    logout(request)
    return redirect('/')



def Signup(request):
    signup  = SignupForm()

    if request.method == 'POST':
        signup  = SignupForm(request.POST)

        if signup.is_valid(): 
            newuser = signup.save()
            newuser = authenticate(
                        request, username = signup.cleaned_data['username'], 
                        password = signup.cleaned_data['password1']
                        )

            if newuser is not None:
                login(request, newuser)

            return HttpResponse('Created and logging in !')

    return render(request, 'account/signup.html', {
        'signup'    : signup
    })


# class LoginView(generic.FormView):
#     form_class = AuthenticationForm
#     success_url = reverse_lazy("signup")
#     template_name = "account/login.html"
    
#     def get_form(self, form_class=None):
#         if form_class is None:
#             form_class = self.get_form_class()
#         return form_class(self.request, **self.get_form_kwargs())
    
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return super().form_valid(form)


# class LogoutView(LoginRequiredMixin, generic.RedirectView):
#     url = reverse_lazy("login")
    
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return super().get(request, *args, **kwargs)


# class SignUp(generic.CreateView):
#     form_class = forms.UserCreateForm
#     success_url = reverse_lazy("login")
#     template_name = "account/signup.html"
