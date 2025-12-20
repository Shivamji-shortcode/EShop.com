from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View
# --- ADD THESE IMPORTS ---
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

@method_decorator(never_cache, name='dispatch')
class Signup(View):
    def get(self, request):
        # --- ADD THIS REDIRECT GUARD ---
        if request.session.get('customer'):
            return redirect('homepage')
        return render(request, 'signup.html')

    def post(self, request):
        # (Keep your existing post logic exactly as it is)
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)

        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            messages.success(request, "Signup successful! Please login to continue ✅")
            return redirect('login')
        else:
            return render(request, 'signup.html', {'error': error_message, 'values': value})

    def validateCustomer(self, customer):
        # (Keep your existing validation logic)
        error_message = None
        if not customer.first_name:
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 8:
            error_message = 'Password must be at least 8 characters long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'

        return error_message