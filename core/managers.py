from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class AccountManager(BaseUserManager):
    use_in_migrations = True

    def create_account(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Учетная запись должна иметь адрес электронной почты')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))
        return self.create_account(email, password, **extra_fields)