from django.shortcuts import render

# Policy page views
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_conditions(request):
    return render(request, 'terms_conditions.html')

def shipping_policy(request):
    return render(request, 'shipping_policy.html')

def refund_policy(request):
    return render(request, 'refund_policy.html')