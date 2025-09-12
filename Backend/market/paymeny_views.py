import  stripe ,uuid
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Cart,Payment,Order,CartItem




stripe.api_key =settings.STRIPE_SECRET_KEY






@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    except Exception:
        return HttpResponse(status=400)

    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_id = session['metadata']['payment_id']

        try:
            payment = Payment.objects.get(id=payment_id)
            payment.status = "Completed"
            payment.transaction_id = session.get("payment_intent")
            payment.save()

            
            order = payment.order
            for item in CartItem.objects.filter(cart=order.cart):
                item.product.quantity -= item.quantity
                item.product.save()
            order.cart.delete()  
        except Payment.DoesNotExist:
            pass

    
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        payment_id = session['metadata']['payment_id']
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.status = "Failed"
            payment.save()
        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)

class CreateCheckoutSession(APIView):
    def post(self, request):
        user= request.user
        cart=Cart.objects.get(user=user)
        order=Order.objects.create(
            user=user,
            cart=cart,
            address=request.data.get('address',"default Address")
        )


        payment=Payment.objects.create(
            order=order,
            user=user,
            amount=cart.total_amount,
            status='Pending',
            transaction_id=str(uuid.uuid4())
        )
        
        session=stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Order {order.id}',
                        },
                        'unit_amount': int(cart.total_amount * 100),
                    },
                    'quantity': 1,
                },

            ],
            mode='payment',
            success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://example.com/cancel',
            metadata={
                'order_id': order.id,
                'payment_id': payment.id
            }


        )
        return Response({'session_id': session.id})
