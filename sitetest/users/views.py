from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from pract.utils import DataMixin
from sitetest import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


# LOGIN_REDIRECT_URL    куда перенаправлять после успешной авторизации
# LOGIN_URL             куда неавторизованного юзера при попытке попасть в закрытую часть сайта
# LOGOUT_REDIRECT_URL   куда после выхода

class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self): # LOGIN_REDIRECT_URL = 'home' в settings.py
    #     return reverse_lazy('home')
# def login_user(request):
    # if request.method == 'POST':
    #     form = LoginUserForm(request.POST)
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         user = authenticate(request, username=cd['username'],
    #                             password=cd['password'])
    #
    #         if user and user.is_active:
    #             login(request, user)
    #             return HttpResponseRedirect(reverse('home'))
    # else:
    #     form = LoginUserForm()
    #
    # return render(request, 'users/login.html', {'form': form})

# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))

# class LogoutUserView(LogoutView):
#
#     def logout_user(self):
#         logout(self.request)
#         return HttpResponseRedirect(reverse('users:login'))

# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})

class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': 'Профиль',
        'default_image': settings.DEFAULT_USER_IMAGE
    }
    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'




class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Корзина'
        return context
     