# 1. Add the correct import for Category
from store.models.category import Category 
from store.models.customer import Customer # Better than * for clarity
from .models.logo_config import LogoConfig

def user_context(request):
    customer = None
    customer_id = request.session.get('customer')
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            customer = None
    return {'customer': customer}

def logo_renderer(request):
    return {
        'logo_data': LogoConfig.objects.first()
    }

def category_renderer(request):
    # 2. Use Capital 'C' Category here
    return {
        'categories': Category.get_all_categories()
    }