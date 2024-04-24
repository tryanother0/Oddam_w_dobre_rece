from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.db.models import Sum
from django.db.models import Count
from django.contrib.auth import login, logout

from django.contrib.auth.models import User

from MainSite.forms import AddUserForm, DonationForm, LoginForm

from .models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        bags_count = Donation.objects.aggregate(bags_count=Sum('quantity'))['bags_count']
        if bags_count == None:
            bags_count = 0


        institutions_with_donations = Donation.objects.all().distinct('institution').count()

        institutions = Institution.objects.all()
        context = {
            'bags_count': bags_count,
            'institutions_with_donations': institutions_with_donations,
            'institutions': institutions
        }
        
        return render(request, "MainSite/index.html", context)

    
class LoginView(FormView):
    template_name = "MainSite/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")
    register_url = reverse_lazy("register")

    def form_valid(self, form):
        user = form.user
        
        login(self.request, user)
        
        return super().form_valid(form) 

    def form_invalid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            return redirect(self.register_url)
        return super().form_invalid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(View):
    form_class = AddUserForm
    template_name = "MainSite/register.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print("get")
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {"form": form}

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        else:
            return render(request, self.template_name, context)


# class AddDonationView(View):
#     def get(self, request, *args, **kwargs):
#         donation_categories = Category.objects.all()
#         institutions = Institution.objects.all()
#         context = {
#             'donation_categories': donation_categories,
#             'institutions': institutions
#         }
#         return render(request, "MainSite/form.html", context)
    

class AddDonationView(View):
    form_class = DonationForm
    template_name = "MainSite/form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        donation_categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {
            'donation_categories': donation_categories,
            'institutions': institutions,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        donation_categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {
            'donation_categories': donation_categories,
            'institutions': institutions,
            'form': form
        }

        if form.is_valid():
            donation = form.save()
            return redirect('index')
        else:
            # Wyświetlenie błędów formularza w terminalu
            print('Formularz nieprawidłowy. Błędy:')
        for field, errors in form.errors.items():
            for error in errors:
                print(f'{field}: {error}')

        return render(request, self.template_name, context)
    

class UserView(View):
    def get(self, request, *args, **kwargs):

        total_bags = Donation.objects.filter(user=request.user).aggregate(total_bags=Count('quantity'))['total_bags']
        total_institutions = Donation.objects.filter(user=request.user).values('institution').distinct().count()

        user = User.objects.get(pk=request.user.pk)
        user_donations = Donation.objects.filter(user=user.pk)
        print(user)
        print(user_donations)
        
        context = {
            'total_bags': total_bags,
            'total_institutions': total_institutions,
            'donations': user_donations
        }
        return render(request, "MainSite/user-site.html", context)
