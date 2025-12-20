from django.shortcuts import render, redirect
from store.models.customer import Customer

def profile_view(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('login')

    customer = Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.phone = request.POST.get('phone')
        customer.house_no = request.POST.get('house_no')
        customer.village = request.POST.get('village')
        customer.city = request.POST.get('city')
        customer.district = request.POST.get('district')
        customer.state = request.POST.get('state')
        customer.pincode = request.POST.get('pincode')
        customer.save()
        return redirect('profile')

    return render(request, 'profile.html', {'customer': customer})
