import math, random, string
from django.utils.text import slugify


def GenerateOTP() : 
    # Declare a digits variable 
    # which stores all digits 
    digits  = "0123456789"
    OTP     = "" 

    # length of password can be changed 
    # by changing value in range 
    for i in range(6) : 
        OTP += digits[math.floor(random.random() * 10)] 

    return OTP


def GenerateUniqueNumber() : 
    # Declare a digits variable 
    # which stores all digits 
    digits = "0123456789"
    unique = "" 

    # length of password can be changed 
    # by changing value in range 
    for i in range(14) : 
        unique += digits[math.floor(random.random() * 10)] 

    return unique


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    """
    This is for a Django project with an key field
    """
    size = random.randint(30, 45)
    link = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(link=link).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return link


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def product_code_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/business_<id>/<filename>
    
	return '{0}/product/code/{1}'.format(instance.product.inventory.id, filename)


def product_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/business_<id>/<filename>
	return '{0}/product/{1}'.format(instance.business.id, filename)