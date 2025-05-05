from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class BvnBackend(BaseBackend):
    def authenticate(self, request, bvn = None, password = None, **kwargs):
        try:
            user = CustomUser.objects.get(bvn=bvn)
            print(bvn,password,"1")
            if user.check_password(password):
                return user
        
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)

        except CustomUser.DoesNotExist:
            return None
