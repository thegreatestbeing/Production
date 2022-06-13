from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, gender, birth_date, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not username:
            raise ValueError("Users must have an unique username")
            
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            gender=gender,
            birth_date=birth_date,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, username, gender, birth_date, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            username,
            gender,
            birth_date,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user