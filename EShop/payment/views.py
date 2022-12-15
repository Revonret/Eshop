import json
import stripe

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from basket.models import Basket
from orders.views import payment_confirmation


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'orderplaced.html')


class Error(TemplateView):
    template_name = 'error.html'


@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    # Po kursie ogarnąć sprawę płatności do końca
    # stripe.api_key = 'pk_test_51MEuyPGJF18TFMYk5BCsGAFafmbIB25yQnhH16MMvhjzIHjO0xjvbqPkjGCzhIl1u00nhJg254bo0pqGgW5UoN7W00XcQvrY5l'
    # intent = stripe.PaymentIntent.create(
    #     amount=total,
    #     currency='pln',
    #     metadata={'userid': request.user.id}
    # ) {'client_secret': intent.client_secret}

    return render(request, 'home.html', )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
