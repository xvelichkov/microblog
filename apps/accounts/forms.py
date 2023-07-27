from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

class ProfileEditForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm):
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email')