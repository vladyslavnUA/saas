from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import stripe
import json
from django.http import JsonResponse
from djstripe.models import Product
from django.contrib.auth.decorators import login_required
import djstripe
from django.http import HttpResponse
from .models import *

def home(request):
    context = {

    }

    return render(request, 'app/index.html', context)

@login_required
def checkout(request):
	products = Product.objects.all()
	return render(request, "app/checkout.html", {"products": products})

def cancel(request):
	# if request.user.is_authenticated:
    if not request.user.is_authenticated:
	    return redirect("home")
    # userid = PayingPeople.find_one(subscription=subscription)
    new = PayingPeople.objects.get(subscription=request.user.subscription.id)
    print(new)
    sub_id = request.user.subscription.id

    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

    try:
        stripe.Subscription.delete(sub_id)
    except Exception as e:
        return JsonResponse({'error': (e.args[0])}, status =403)
    

@login_required
def create_sub(request):
	if request.method == 'POST':
	    # Reads application/json and returns a response
	    data = json.loads(request.body)
	    payment_method = data['payment_method']
	    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

	    payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
	    djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)


	    try:
	        # This creates a new Customer and attaches the PaymentMethod in one API call.
	        customer = stripe.Customer.create(
	            payment_method=payment_method,
	            email=request.user.email,
	            invoice_settings={
	                'default_payment_method': payment_method
	            }
	        )

	        djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
	        request.user.customer = djstripe_customer
	       

	        # At this point, associate the ID of the Customer object with your
	        # own internal representation of a customer, if you have one.
	        # print(customer)

	        # Subscribe the user to the subscription created
	        subscription = stripe.Subscription.create(
	            customer=customer.id,
	            items=[
	                {
	                    "price": data["price_id"],
	                },
	            ],
	            expand=["latest_invoice.payment_intent"]
	        )

	        djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

	        request.user.subscription = djstripe_subscription
	        request.user.save()

	        return JsonResponse(subscription)
	    except Exception as e:
	        return JsonResponse({'error': (e.args[0])}, status =403)
	else:
		return HTTPresponse('requet method not allowed')

def complete(request):
	return render(request, 'app/complete.html')