from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm , UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy

# Create your views here.


class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def get_success_url(self):
        return reverse_lazy('homepage')


# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#             return reverse_lazy('homepage')
    
    # def get_success_url(self):
    #     if self.request.user.is_authenticated:
    #         logout(self.request)
    #     return self.get_redirect_url('homepage')


# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request.user)
#         return reverse_lazy('homepage')
    
class UserLogoutView(View):
    def get_success_url(self):
        return reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(self.get_success_url())
    

class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})