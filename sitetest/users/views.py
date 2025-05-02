from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from carts.models import Cart
from orders.models import Order, OrderItem
from pract.utils import DataMixin
from sitetest import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm

from django.contrib import messages
from django.db.models import Prefetch


# LOGIN_REDIRECT_URL    куда перенаправлять после успешной авторизации
# LOGIN_URL             куда неавторизованного юзера при попытке попасть в закрытую часть сайта
# LOGOUT_REDIRECT_URL   куда после выхода

class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    # extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('users:logout'):
            return redirect_page
        return reverse_lazy('home')



    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()
        
        if user:
            auth.login(self.request, user)
            if session_key: 

                # forgot_carts = Cart.objects.filter(user=user)
                # if forgot_carts.exists():
                #     forgot_carts.delete()

                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
            return HttpResponseRedirect(self.get_success_url())




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Карамелька - Авторизация'
        return context






class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:profile')
    

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)





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
    


    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Кабинет'
        context['orders'] = Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")
        return context


class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Корзина'
        return context




class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'





     