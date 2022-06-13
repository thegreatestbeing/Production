#import math, random
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import activate, ugettext_lazy as _

# Create your models here.
from Account.managers import UserManager
from Account.validators import image
from Business.extras import GENDER
from Business.utils import GenerateOTP, random_string_generator, unique_key_generator


DEFAULT_ACTIVATION_MINUTES = getattr(settings, 'DEFAULT_ACTIVATION_MINUTES', 60)


def user_profile_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return '{0}/profile/{1}'.format(instance.user.id, filename)


class User(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(_('email address'), unique=True)
    username        = models.CharField(_('username'), unique=True, max_length=32, blank=True)
    first_name      = models.CharField(_('first name'), max_length=30, blank=True)
    last_name       = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined     = models.DateTimeField(_('date joined'), auto_now_add=True)
    gender          = models.CharField(max_length=1, blank=True, choices=GENDER)
    birth_date      = models.DateField(null=True, blank=True)
    is_active       = models.BooleanField(_('active'), default=True)
    is_staff        = models.BooleanField(default=False)

    objects         = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'gender', 'birth_date']

    class Meta:
        verbose_name        = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        # Sends an email to this user
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_user(self):
        return get_object_or_404(User, id__iexact=self.kwargs.get('pk'))


class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_profile_directory_path, validators=[image])


class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now         = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_MINUTES)
        # does my object have a timestamp in here 
        end_range   = now
        return self.filter(
                    activated   = False,
                    expired     = False
                ).filter(
                    timestamp__gt   = start_range,
                    timestamp__lte  = end_range
                )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()
    
    def email_exists(self, email):
        return self.get_queryset().filter(
                    Q(email         = email) | 
                    Q(user__email   = email)
                ).filter(
                    activated       = False
                )


class EmailActivation(models.Model):
    activated   = models.BooleanField(default=False)
    email       = models.EmailField()
    expired     = models.BooleanField(default=False)
    link        = models.CharField(max_length=120, blank=True, null=False)
    OTP         = models.CharField(max_length=120, blank=True, null=True)
    valid       = models.DateTimeField(null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update      = models.DateTimeField(auto_now=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    objects     = EmailActivationManager()

    def __str__(self) -> str:
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() # 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            # pre activation user signal
            user = self.user
            user.is_active = True
            user.save()
            
            # post activation signal for user
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.link = None
        self.save()
        if self.link is not None:
            return True
        return False 

    def send_activation(self):
        if not self.activated and timezone.now() <= self.valid:
            if self.OTP:
                # base_url = getattr(settings, 'BASE_URL', 'https://www.pythonecommerce.com')
                # key_path = reverse("account:email-activate", kwargs={'key': self.key}) # use reverse
                # path = "{base}{path}".format(base=base_url, path=key_path)
                # OTP = self.OTP
                context = {
                    'OTP'   : self.OTP,
                    'link'  : self.link,
                    'email' : self.email
                }
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = '{0} is your Hāsh comfirmation code'.format(self.OTP)
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                            subject,
                            txt_,
                            from_email,
                            recipient_list,
                            html_message=html_,
                            fail_silently=False,
                    )
                return sent_mail
        return False

    def send_user_activated(self):            
        # base_url = getattr(settings, 'BASE_URL', 'https://www.pythonecommerce.com')
        # key_path = reverse("account:email-activate", kwargs={'key': self.key}) # use reverse
        # path = "{base}{path}".format(base=base_url, path=key_path)
        # OTP = self.OTP
        name    = self.user.first_name
        user    = self.user.username
        profile = ''
        for i in Profile.objects.filter(user=self.user):
            profile = i.profile_pic
        context = {
            'username'  : user,
            'name'      : name,
            'profile'   : profile,
            'email'     : self.email
        }
        txt_ = get_template("registration/emails/thanks.txt").render(context)
        html_ = get_template("registration/emails/thanks.html").render(context)
        subject = 'Account Verified'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        sent_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False,
            )
        return sent_mail


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.expired:
        if not instance.OTP:
            instance.OTP    = GenerateOTP()
            instance.link   = unique_key_generator(instance)
        else : 
            instance.OTP    = GenerateOTP()
            instance.link   = unique_key_generator(instance)
            
pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_reciever(sender, instance, created, *args, **kwargs):
    if created:
        valid_till = timezone.now() + timedelta(minutes=4)
        obj        = EmailActivation.objects.create(user=instance, email=instance.email, valid=valid_till)
        obj.send_activation()

post_save.connect(post_save_user_reciever, sender=User)


def activated_user(sender, instance, created, *args, **kwargs):
    if instance.activated == True:
        # obj     = EmailActivation.objects.get_or_create(user=instance)
        instance.send_user_activated()        
post_save.connect(activated_user, sender=EmailActivation)


