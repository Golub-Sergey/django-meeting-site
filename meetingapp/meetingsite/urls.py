from django.urls import path


from .views import (BaseView, ProfileView, 
    RegistrationUserView, ThanksView,
    CreateUserProfileView, LoginView,
    LogoutUserView, ProfileUpdateView,
    CustomUserUpdateView, DialogView)


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<user_profile>', ProfileView.as_view(), name='user_profile'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('create_profile/', CreateUserProfileView.as_view(), name='create_profile'),
    path('update_profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('update_user/', CustomUserUpdateView.as_view(), name='update_user'),
    path('dialogs/', DialogView.as_view(), name='dialog_view'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout')
]