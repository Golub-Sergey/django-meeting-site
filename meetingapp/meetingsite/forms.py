from django import forms
from .models import UserProfile, CustomUser, Images
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType


class UserProfileForm(forms.ModelForm):

    profile_image = forms.ImageField(required=False)

    class Meta:

        model = UserProfile
        fields = [
            'bio'
        ]
        exclude = [
            'username',
            'img'
        ]
        labels = {
            'bio': 'О себе'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].label = 'Добавить картинку'

    def save(self, commit=True):
        instance = super(UserProfileForm, self).save(commit=False)
        instance.bio = self.cleaned_data['bio']
        instance.save()
        if self.cleaned_data['profile_image']:
            Images.objects.create(obj=instance, image=self.cleaned_data['profile_image'])
        return instance
        

class RegistrationUserForm(forms.ModelForm):

    password_check = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField(required=False)
    
    class Meta:

        model = CustomUser
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email',
            'gender',
            'age'
        ]
        exclude = [
            'img'
        ]

        labels = {
            'username': 'Логин',
            'password': 'Пароль',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Ваша почта',
            'gender': 'Ваш пол',
            'age': 'Ваш возраст',
            'avatar': 'Ваше фото'
        }
        
        help_texts = {
            'password': 'Придумайте пароль',
            'email': 'Пожалуйста, укажите актуальный адрес'
        }   
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['avatar'].label = 'Ваше фото'

    def save(self, commit=True):
        instance = super(RegistrationUserForm, self).save(commit=False)
        instance.username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        instance.set_password(password)
        instance.first_name = self.cleaned_data['first_name']
        instance.last_name = self.cleaned_data['last_name']
        instance.email = self.cleaned_data['email']
        instance.age = self.cleaned_data['age']
        instance.gender = self.cleaned_data['gender'] 
        instance.save()
        if self.cleaned_data['avatar']:
            Images.objects.create(obj=instance, image=self.cleaned_data['avatar'])
        return {'username': instance.username, 'password': password}

    # override method for validate form
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином уже зарегистрирован в системе!')
        if password != password_check:
            raise forms.ValidationError('Ваши пароли не совпадают! Попробуйте снова!')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с данным почтовым адресом уже зарегистрирован!')


class UpdateCustomUserForm(forms.ModelForm):

    avatar = forms.ImageField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].label = 'Ваше фото'

    class Meta:

        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'age',          
        ]

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Ваша почта',
            'age': 'Возраст',  
        }

        exclude = [
            'username',
            'gender',
            'img',
            'password'
        ]

    def save(self, commit=True):
        instance = super(UpdateCustomUserForm, self).save(commit=False)
        instance.first_name = self.cleaned_data['first_name']
        instance.last_name = self.cleaned_data['last_name']
        instance.email = self.cleaned_data['email']
        instance.age = self.cleaned_data['age']
        instance.save()
        if self.cleaned_data['avatar']:
            try:
                content_type = ContentType.objects.get_for_model(instance)
                avatar = self.cleaned_data['avatar']
                new_image = Images.objects.get(content_type__pk=content_type.id, object_id=instance.id)
                new_image.image=avatar
                new_image.save()
            except:
                Images.objects.create(obj=instance, image=avatar)
        return instance

class LoginForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password'
        ]
        labels = {
            'username': 'Ваш логин',
            'password': 'Пароль'
        }
        widgets = {
            'password': forms.PasswordInput() 
        }

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином не зарегистрирован в системе!')
        
        user = CustomUser.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')

class ImageUploadForm(forms.Form):

    image = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Добавить картинку'

class SearchForm(forms.Form):

    query_form_data = forms.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query_form_data'].widget.attrs.update({
            'class': 'form-control mr-sm-2',
            'type': 'search',
            'placeholder': 'Search',
            'aria-label': 'Search'})

    def get_searched_queryset(self, queryset):
        if 'query_form_data' in self.cleaned_data and self.cleaned_data['query_form_data']:
            queryset = queryset.filter(
                Q(first_name__icontains=self.cleaned_data['query_form_data']) |
                Q(last_name__icontains=self.cleaned_data['query_form_data']) 
                )
        return queryset