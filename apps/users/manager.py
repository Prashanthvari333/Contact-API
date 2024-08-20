from django.contrib.auth.base_user import BaseUserManager
class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, phone_number, username, password=None, email=None,is_staff=False, is_admin=False):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        if not username:
            raise ValueError("Users must have a name")

        user = self.model(phone_number=phone_number, username = username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create(self, phone_number, password=None, is_staff=False, is_admin=False):
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(phone_number=phone_number, is_staff=is_staff, is_admin=is_admin)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create(phone_number,password, is_staff=True, is_admin=True)
        return user

