from django.shortcuts import render
from django.views import View
from store.models.orders import Order
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import razorpay
import json


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'orders.html', {'orders': orders})


# ✅ Create Razorpay Order
@csrf_exempt
def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount_rupees = int(float(data.get("amount_rupees", 0)))
            amount_paise = amount_rupees * 100  # Convert to paise

            # 🔑 Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # 🧾 Create order
            order = client.order.create({
                "amount": amount_paise,
                "currency": "INR",  # Important!
                "payment_capture": "1"
            })

            return JsonResponse({"razorpay_order": order})
        except Exception as e:
            print("❌ Error creating order:", str(e))
            return JsonResponse({"error": str(e)})


# ✅ Verify Razorpay Payment
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            params_dict = {
                "razorpay_order_id": data.get("razorpay_order_id"),
                "razorpay_payment_id": data.get("razorpay_payment_id"),
                "razorpay_signature": data.get("razorpay_signature")
            }

            # ✅ Verify signature
            client.utility.verify_payment_signature(params_dict)
            return JsonResponse({"status": "success"})

        except Exception as e:
            print("❌ Verification failed:", str(e))
            return JsonResponse({"status": "failed", "error": str(e)})
