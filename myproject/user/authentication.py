from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class UserIDAuthBackend(ModelBackend):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(user_id=user_id)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
