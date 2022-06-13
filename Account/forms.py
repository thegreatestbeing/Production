from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm

from django.urls import reverse, reverse_lazy

from Account.models import EmailActivation
from django import forms

class SignupForm(UserCreationForm):
    class Meta:
        fields = ("first_name", "last_name", "email", "username", "birth_date", "gender")
        model = get_user_model()
        widgets = {
        	'username': forms.TextInput(attrs={
        		'required': 'True',
                'id': 'user',
                'name': 'user_name'
        		})
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')


class LoginForm(forms.Form):
    email    = forms.CharField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email  = data.get("email")
        password  = data.get("password")
        qs = EmailActivation.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(activated=False)
            if not_active.exists():
                ## not active, check email activation
                link = reverse("account:resend-activation")
                reconfirm_msg = """Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """.format(resend_link = link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("This user is inactive.")
            else:
                user = authenticate(request, username=email, password=password)
        if request.user is None:
            raise forms.ValidationError("Invalid credentials")

        return data

    # def form_valid(self, form):
    #     request = self.request
    #     next_ = request.GET.get('next')
    #     next_post = request.POST.get('next')
    #     redirect_path = next_ or next_post or None
    #     email  = form.cleaned_data.get("email")
    #     password  = form.cleaned_data.get("password")
        
    #     print(user)
    #     if user is not None:
    #         if not user.is_active:
    #             print('inactive user..')
    #             messages.success(request, "This user is inactive")
    #             return super(LoginView, self).form_invalid(form)
    #         login(request, user)
    #         user_logged_in.send(user.__class__, instance=user, request=request)
    #         try:
    #             del request.session['guest_email_id']
    #         except:
    #             pass
    #         if is_safe_url(redirect_path, request.get_host()):
    #             return redirect(redirect_path)
    #         else:
    #             return redirect("/")
    #     return super(LoginView, self).form_invalid(form)


class OTPForm(forms.Form):
    OTP         = forms.CharField()


class ReactivateEmailForm(forms.Form):
    email       = forms.EmailField()

    def clean_email(self):
        email   = self.cleaned_data.get('email')
        qs      = EmailActivation.objects.email_exists(email) 
        if not qs.exists():
            register_link = reverse("register")
            msg = """This email does not exists, would you like to <a href="{link}">Sing Up</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email



