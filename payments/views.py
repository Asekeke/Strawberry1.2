from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
import stripe
import json
import os
from dotenv import load_dotenv
from products.models import Cart

# Загружаем секретные переменные из .env
load_dotenv()
stripe.api_key = os.getenv('SECRET_KEY')


# Функция для создания checkout сессии
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            print("Initial---------", request.POST)

            # Получаем продукты из корзины пользователя
            cart_products = Cart.objects.filter(user=request.user).values()
            cart_product_list = list(cart_products)

            # Сериализуем список продуктов корзины в JSON
            serialized_cart_products = json.dumps(cart_product_list, cls=DjangoJSONEncoder)
            print(serialized_cart_products)

            # Получаем сумму для оплаты
            subtotal = Cart.subtotal_product_price(request.user)
            amount = subtotal * 100  # Сумма в центах

            # Создаем PaymentIntent с нужной суммой и валютой
            intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency='usd',
                automatic_payment_methods={'enabled': True},
                metadata={'cart_products': serialized_cart_products},
            )

            print(intent.client_secret)
            return JsonResponse({'clientSecret': intent.client_secret})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)


# Функция для отображения деталей платежа
def display_payment_details(request):
    cart_products = Cart.objects.filter(user=request.user)

    context = {
        'cart_products': cart_products,
        'payable': Cart.subtotal_product_price(request.user)
    }

    return render(request, 'payments/payment.html', context)


# Функция для обработки успешного платежа
def payment_success(request):
    payment_intent_id = request.GET.get('payment_intent')
    email = request.user.email

    # После успешного платежа размещаем заказ
    oder_placed = placed_oder(request)

    # Ищем клиента по email
    get_customer = stripe.Customer.search(query=f'email:"{email}"')
    if get_customer:
        customer = get_customer['data'][0]
    else:
        customer = stripe.Customer.create(
            name=request.user.first_name,
            email=request.user.email,
            description="Creating user for purchasing product"
        )
        print(customer)

    # Обновляем существующий PaymentIntent
    payment_intent = stripe.PaymentIntent.modify(
        payment_intent_id,
        metadata={'oder_id': oder_placed},
        customer=customer
    )
    print(payment_intent)
    amount_paid = payment_intent['amount_received'] / 100

    context = {
        "payment_intent": payment_intent,
        "amount_paid": amount_paid
    }

    return render(request, 'payments/success.html', context)


# Функция для применения купона
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('cupon_code')

        # Логика для проверки и применения купона (замените на вашу)
        if coupon_code == "valid_coupon_code":  # Пример, замените на реальную логику
            # Логика применения купона
            messages.success(request, "Купон успешно применен!")
        else:
            messages.error(request, "Неверный купон!")

    return redirect('display_payment_details')  # Перенаправляем обратно на страницу с деталями платежа