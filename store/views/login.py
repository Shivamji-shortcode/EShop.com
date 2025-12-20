from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
# --- ADD THESE IMPORTS ---
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

@method_decorator(never_cache, name='dispatch')
class Login(View):
    return_url = None

    def get(self, request):
        # --- ADD THIS REDIRECT GUARD ---
        if request.session.get('customer'):
            return redirect('homepage')
            
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer and check_password(password, customer.password):
            request.session['customer'] = customer.id
            messages.success(request, f"Welcome, {customer.first_name} 👋")
            if Login.return_url:
                return HttpResponseRedirect(Login.return_url)
            else:
                Login.return_url = None
                return redirect('homepage')
        else:
            error_message = 'Email or Password invalid !!'

        return render(request, 'login.html', {'error': error_message})

# Add decorator to logout as well for extra security
@never_cache
def logout(request):
    request.session.clear()
    return redirect('login')