from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        auth_user = Group.objects.get(name='auth users')
        user.groups.add(auth_user)
        return user


