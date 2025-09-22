from django.contrib import admin


from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.models import Role

from .models import (
    Product,Order,Owner,ProductComments,ProductMessage
    ,Consultant,ConsultantPost,RequestTobeOwer,ConsultantFollow,
    ProductDiscount
    ,Payment,Testimonials,CustomerSupport,OrderItem,RequestTobeConsultant
)

# Register your models here.



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'owner', 'price', 'quantity','description','product_image']
    list_filter = ['owner', 'price']
    search_fields = ['product_name', 'description']
    list_per_page = 10


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'discount_percentage', 'owner', 'created_at']
    search_fields = ['product__product_name', 'customer__username', 'owner__user__username']
    list_per_page = 10

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'farming_name', 'location']
    search_fields = ['user__username', 'farming_name']
    list_per_page = 10
    





@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'address']
    # search_fields = ('user__username', 'product__name', 'address')
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    search_fields = ['order__id', 'product__product_name']
    list_per_page = 10


@admin.register(ProductMessage)
class ProductMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'product', 'message', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'product__name', 'message']
    list_per_page = 10



@admin.register(ProductComments)
class ProductCommentsAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'comment', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    list_per_page = 10



@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display=["user","location"]
    search_fields=["location"]

    




@admin.register(ConsultantPost)
class ConsultantPostAdmin(admin.ModelAdmin):
    list_display=["post_title","created_at"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=["user","amount","status","payment_date","transaction_id"]
    



@admin.register(RequestTobeOwer)
class    RequestTobeOwerAdmin(admin.ModelAdmin):
        list_display=["user","farming_name","location"]
        search_fields=["user__username","farming_name","location"]
        list_per_page=10
        actions =["approve_request","reject_request"]

        def send_seller_email(self, user, approved=True):
            subject ="Seller Request Approved" if approved else "Seller Request Rejected"
            context={
                'subject':subject,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'approved':approved,
            
            }

            html_content=render_to_string('emails/seller_request.html',context)
            text_content=strip_tags(html_content)

            email=EmailMultiAlternatives(
                subject,
                text_content,
                "Ngererayo Market <gihozoismail@gmail.com> ",
                  [user.email]
            )
            email.attach_alternative(html_content,"text/html")
            email.send()
        def  approve_request(self, request,queryset):
            for req in queryset:

                Owner.objects.create(
                    user=req.user,
                    farming_name=req.farming_name,
                    location=req.location,
                )
                req.user.role.add(Role.objects.get_or_create(name="farmer")[0])
                req.user.save()

                self.send_seller_email(req.user,approved=True)
                req.delete()


            self.message_user(request, "Request approved successfully")
        approve_request.short_description="approved selected request"


        def reject_request(self, request,queryset):
            for req in queryset:
                self.send_seller_email(req.user,approved=False)
                req.delete()
                self.message_user(request, "Request rejected successfully")
        reject_request.short_description="rejected selected request"  



@admin.register(RequestTobeConsultant)
class RequestTobeConsultantAdmin(admin.ModelAdmin):
    list_display=["user","location","status"]
    search_fields=["user__username","location","status"]
    list_per_page=10
    actions =["approve_request","reject_request"]
    def send_consultant_email(self,user, approved=True):

        subject="Consultant request approved" if approved else "Consultant request rejected"
        context={
            "subject":subject,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "approved":approved

            
        } 
        html_content=render_to_string("emails/consultant_request.html",context)
        text_content=strip_tags(html_content)
        email=EmailMultiAlternatives(
            subject,
            text_content,
            "Ngererayo <gihozoismail@gmail.com>",
            [user.email]
        )
        email.attach_alternative(html_content,"text/html")
        email.send()

    def approve_request(self, request, queryset):
         for req in queryset:
                Consultant.objects.create(
                    user=req.user,
                    location=req.location,


                )
                req.user.role.add(Role.objects.get_or_create(name="consultant")[0])
                req.user.save()
                self.send_consultant_email(req.user, approved=True)
                req.delete()
                self.message_user(request,"request approved successfully")

    approve_request.short_description = "request approved"
    def reject_request(self,request,queryset):
        for req in queryset:
            self.send_consultant_email(req.user, approved=False)
            req.delete()
            self.message_user(request,"request rejected")
    reject_request.short_description="reject request"                    


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display=["user","testimonial","created_at"]
    search_fields=["user__username","testimonial"]





@admin.register(CustomerSupport)
class CustomerSupportAdmin(admin.ModelAdmin):
    list_display=["full_name","email","status","subject","created_at"]
    search_fields=["full_name","email","status","subject"]
    list_per_page=10



@admin.register(ConsultantFollow)
class ConsultantFollowAdmin(admin.ModelAdmin):
    list_display=["user","consultant","created_at"]
    search_fields=["user__username","consultant__user__username"]








    
    
