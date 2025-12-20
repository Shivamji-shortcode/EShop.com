from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Product
from store.models.orders import Order

# ✅ Razorpay imports
import razorpay
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
import json
import hmac
import hashlib


# ✅ Main Checkout View
class CheckOut(View):
    def get(self, request):
        """
        Render checkout page with total cart amount and Razorpay key.
        """
        cart = request.session.get('cart', {})
        products = Product.get_products_by_id(list(cart.keys()))

        total = 0
        for product in products:
            total += product.price * cart.get(str(product.id), 0)

        context = {
            'total_amount': total,
            'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID
        }

        return render(request, 'checkout.html', context)

    def post(self, request):
        """
        Handles placing orders from cart after successful payment.
        """
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart', {})
        products = Product.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(
                customer=Customer(id=customer),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id))
            )
            order.save()

        # Clear cart after placing order
        request.session['cart'] = {}

        return redirect('orders')


# ✅ Razorpay Order Creation
@require_POST
def create_order(request):
    """
    Create a Razorpay order for the given total amount (in rupees).
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        amount_rupees = float(data.get("amount_rupees", 0))
        amount_paise = int(amount_rupees * 100)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": "1"
        })

        return JsonResponse({"razorpay_order": razorpay_order})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ✅ Razorpay Payment Verification
@require_POST
def verify_payment(request):
    """
    Verify payment signature from Razorpay after successful payment.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")

        if not (razorpay_payment_id and razorpay_order_id and razorpay_signature):
            return HttpResponseBadRequest("Missing fields")

        # Verify signature using HMAC SHA256
        body = f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8')
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()

        if expected_signature != razorpay_signature:
            return JsonResponse({"status": "failure", "reason": "signature mismatch"}, status=400)

        # ✅ Signature valid → payment successful
        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
