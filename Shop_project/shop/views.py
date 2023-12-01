from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import stripe
from django.conf import settings
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


@require_GET
def buy_item(request, item_id):
    item = Item.objects.get(pk=item_id)

    # line_item с ценой тестового товара, созданного в Stripe для проверки работы оплаты. Соответствует item_id = 1.
    line_item = {
        'price': settings.TEST_PRODUCT_PRICE,
        'quantity': 1,
    }

    # # Так будет выглядеть реальный line_item, передающий данные о товаре в Stripe. Можно добавить и другие параметры.
    # line_item = {
    #     'price': int(item.price * 100),  # цена в центах
    #     'quantity': 1,
    #     'name': item.name,
    #     'description': item.description,
    # }

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[line_item],
        mode='payment',
        success_url=request.build_absolute_uri(item.get_absolute_url()),
        cancel_url=request.build_absolute_uri(item.get_absolute_url()),
    )

    return JsonResponse({'session_id': session.id})


@require_GET
def view_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    csrf_token = request.COOKIES.get('csrftoken', '')
    context = {'item': item, 'csrf_token': csrf_token, 'public_key': settings.STRIPE_PUBLIC_KEY}
    return render(request, 'item.html', context)
