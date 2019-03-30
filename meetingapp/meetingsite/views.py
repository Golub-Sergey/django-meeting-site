from django.shortcuts import redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.views.generic import View, TemplateView, FormView, UpdateView, ListView
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile, Images, CustomUser
from .forms import (RegistrationUserForm, UserProfileForm, 
    LoginForm, ImageUploadForm, 
    UpdateCustomUserForm, SearchForm)
from django.contrib.auth.views import LogoutView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from chatengine.models import Group
from django.db.models import Q


class BaseView(TemplateView):
    template_name = 'meetingsite/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.all()
        context['form'] = SearchForm(data=self.request.GET or None)
        if context['form'] and context['form'].is_valid():
            user = context['form'].get_searched_queryset(user)
        context.update({
            'users': user
        })
        return context

class DialogView(ListView):
    template_name = 'meetingsite/dialog.html'
    model = Group
    
    def get_queryset(self):
        queryset = Group.objects.filter(Q(group_name__icontains=self.request.user) | 
             Q(username__icontains=self.request.user)).values('group_name').distinct()
        return queryset


@method_decorator(login_required, 'dispatch')
class ProfileView(FormView):
    template_name = 'meetingsite/profile.html'
    form_class = ImageUploadForm
    success_url = '/base/profile/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs:
            username = self.kwargs['user_profile']
            user = CustomUser.objects.get(username=username)
            userprofile = UserProfile.objects.all().prefetch_related('img').get(username__username=username)
            current_user = False
        else:
            user = CustomUser.objects.get(username=self.request.user)
            try:
                userprofile = UserProfile.objects.get(username=self.request.user)
            except:
                userprofile = None
            current_user = True
        context.update({
            'user': user,
            'userprofile': userprofile,
            'current_user': current_user
        })
        return context

    def form_valid(self, form):
        image = form.cleaned_data['image']
        user = UserProfile.objects.get_or_create(username=self.request.user)
        Images.objects.create(obj=user[0], image=image)
        return redirect(self.get_success_url())
        

@method_decorator(login_required, 'dispatch')
class ProfileUpdateView(UpdateView):
    template_name = 'meetingsite/update_profile.html'
    form_class = UserProfileForm
    success_url = '/base/profile/'

    def get_object(self):
        return get_object_or_404(UserProfile, username=self.request.user)

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


@method_decorator(login_required, 'dispatch')
class CustomUserUpdateView(UpdateView):
    template_name = 'meetingsite/update_user.html'
    form_class = UpdateCustomUserForm
    success_url = '/base/profile/'

    def get_object(self):
        return get_object_or_404(CustomUser, username=self.request.user)

    def get_initial(self):
        initial = super().get_initial()
        updatedUser = CustomUser.objects.get(username = self.request.user)
        try:
            image = updatedUser.img.first()
            initial.update({'avatar': image.image})
        except:
            initial = None
        return initial

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())
    

class RegistrationUserView(FormView):
    template_name = 'meetingsite/registration.html'
    form_class = RegistrationUserForm
    success_url = '/base/thanks/'

    def form_valid(self, form):
        new_user = form.save()
        login_user = authenticate(username=new_user['username'], password=new_user['password'])
        if login_user:
            login(self.request, login_user)
        return redirect(self.get_success_url())


@method_decorator(login_required, 'dispatch')
class CreateUserProfileView(FormView):
    template_name = 'meetingsite/create_profile.html'
    form_class = UserProfileForm
    success_url = '/base/profile/'

    def form_valid(self, form):
        form.save(self.request.user)
        return redirect(self.get_success_url())


class ThanksView(TemplateView):
    template_name = 'meetingsite/thanks.html'


class LoginView(FormView):
    template_name = 'meetingsite/login.html'
    form_class = LoginForm
    success_url = '/base/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(self.request, login_user)
        return redirect(self.get_success_url())


class LogoutUserView(LogoutView):
    next_page='base'
