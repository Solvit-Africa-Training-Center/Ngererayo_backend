import  stripe 


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .models import Payment,Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request,order_id):
        try:
            order=Order.objects.get(id=order_id,user=request.user)
        except Order.DoesNotExist:
            return Response("Order not found",status=status.HTTP_404_NOT_FOUND)
        total_amount=sum(item.product.price*item.quantity for item in order.items.all())
        payment,created=Payment.objects.get_or_create(
            order=order,
            defaults={
                 "user": request.user,
                "amount": total_amount,
                "status": "Pending",
                "transaction_id": f"temp-{order.id}",
            }
        )

        intent=stripe.PaymentIntent.create(
            amount=int(total_amount*100),
            currency="usd",
            metadata={"order_id": order.id, "user_id": request.user.id},
           
        )

        payment.transaction_id=intent.id
        payment.save()


        return Response({
            "messages":"payment created successfully",
            "payment":
            {
                
                "id": payment.id,
                "amount": str( payment.amount),
                "status": payment.status,
                "transaction_id": payment.transaction_id,
                "order_id": payment.order.id,
            },
            "client_key":intent.client_secret,
            "publishable_key":settings.STRIPE_PUBLIC_KEY,
        }, status=status.HTTP_201_CREATED)  






@csrf_exempt

def stripe_webhook(request):
    payload=request.body
    sig_header=request.META.get['HTTP_STRIPE_SIGNATURE']
    endpoint_secret=settings.STRIPE_WEBHOOK_SECRET
    try:
        event=stripe.webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

    if event["type"] =="payment_intent.succeeded":
        intent=event["data"]["object"]
        transaction_id=intent["id"]
        Payment.objects.filter(transaction_id=transaction_id).update(status="Completed")
    elif event["type"] =="payment_intent.payment_failed":
        intent=event["data"]["object"]
        transaction_id=intent["id"]
        Payment.objects.filter(transaction_id=transaction_id).update(status="Failed")



    return JsonResponse({'success': True})        
    