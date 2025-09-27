from django.db import models
from decimal import Decimal
from  cloudinary.models import CloudinaryField
from accounts.models import CustomUser

# Create your models here.


class Owner(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    farming_name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    class Meta:
        verbose_name="Owner"
        verbose_name_plural="Owners"
    def __str__(self):
        return self.user.first_name + " " + self.farming_name
    


class Product(models.Model):
    owner=models.ForeignKey(Owner,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField()
    product_image=CloudinaryField("image",folder='product_images')
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at=models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name="Product",
        verbose_name_plural="Products" 
    def __str__(self):
        return self.product_name
class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image=models.ImageField(upload_to='product_images')
    class Meta:
        verbose_name="ProductImage"
        verbose_name_plural="ProductImages"
    def __str__(self):
        return f"Image for {self.product.product_name}"

class ProductDiscount(models.Model):
    DISCOUNT_TYPE_PERCENT='percent'
    DISCOUNT_TYPE_FIXED='Fixed'
    DISCOUNT_TYPE_CHOICES=[
        (DISCOUNT_TYPE_PERCENT,'Percentage'),
        (DISCOUNT_TYPE_FIXED,'Fixed-amount')
    ]
    owner=models.ForeignKey(Owner, on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="discounts")
    customer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    discount_type=models.CharField(max_length=20,choices=DISCOUNT_TYPE_CHOICES,default=DISCOUNT_TYPE_PERCENT)
    amount=models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage or fixed amount")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('customer','product')
        verbose_name="ProductDiscount"
        verbose_name_plural="ProductDiscounts"
    def get_discounted_price(self):
        price=self.product.price
        if self.discount_type ==self.DISCOUNT_TYPE_PERCENT:
            factor=(Decimal("100")-self.amount)/ Decimal("100")
            return (price*factor).quantize(Decimal("0.01"))
        else:
            discounted=price-self.amount
            return discounted if discounted >Decimal("0.00")  else Decimal("0.00") 
    def __str__(self):
        if self.discount_type == self.DISCOUNT_TYPE_PERCENT:
            return f"{self.amount}% discount on {self.product.product_name} for {self.customer.username}"
        else:
            return f"{self.amount} off {self.product.product_name} for {self.customer.username}"

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="Order"
        verbose_name_plural="Orders"

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    class Meta:
        verbose_name="OrderItem"
        verbose_name_plural="OrderItems"
    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in Order {self.order.id}"


class ProductMessage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        verbose_name="ProductMessage"
        verbose_name_plural="ProductMessages"

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} about {self.product.product_name}"


class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name="ProductComment"
        verbose_name_plural="ProductComments"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.product_name}"
    





class Consultant(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    location=models.CharField(max_length=200)
    class Meta:
        verbose_name="Consultant"
        verbose_name_plural="Consultants"
    def __str__(self):
        return self.user.first_name   

class ConsultantPost(models.Model):
    consultant=models.ForeignKey(Consultant,on_delete=models.CASCADE)
    post_title=models.CharField(max_length=100)
    post_description=models.TextField(blank=True,null=True)
    post_image=CloudinaryField("image",folder='post_images',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="ConsultantPost"
        verbose_name_plural="ConsultantPosts"
    def __str__(self):
        return self.post_title


class ConsultantFollow(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    consultant=models.ForeignKey(Consultant,on_delete=models.CASCADE,related_name='followers')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'consultant')
        verbose_name="ConsultantFollow"
        verbose_name_plural="ConsultantFollows"


    def __str__(self):
        return f"{self.user.username} follows {self.consultant.user.username}"    


class RequestTobeConsultant(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE )
    location=models.CharField(max_length=200)
    national_id=models.FileField(upload_to='national_id_files',null=True,blank=True)
    license=models.FileField(upload_to='license_files')
    STATUS_CHOICES=[
        ("pending","pending"),
        ("approved","approved"),
        ("rejected","rejected")
    ]
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="pending")


class RequestTobeOwer(models.Model):
    STATUS_CHOICES=[
        ("pending","pending"),
        ("approved","approved"),
        ("rejected","rejected")
    ]
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    farming_name=models.CharField(max_length=100)
    location=models.CharField(max_length=200) 
    national_id=models.FileField(upload_to='national_id_files',null=True,blank=True)
    license=models.FileField(upload_to='license_files')
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="pending")
    class Meta:
        verbose_name="Request to be Owner"
        verbose_name_plural="Requests to be Owners"
    def __str__(self):
        return f"Request to be owner of {self.farming_name} by {self.user.username}"





class Payment(models.Model):

    Status_Choice=[
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Failed','Failed')
    ]
    order=models.OneToOneField(Order,on_delete=models.CASCADE, related_name='payment',null=True,blank=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=10,choices=Status_Choice,default='Pending')
    payment_date=models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name="Payment"
        verbose_name_plural="Payments"
    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} on {self.payment_date}"
    





class Testimonials(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    testimonial=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="Testimonial"
        verbose_name_plural="Testimonials"




class CustomerSupport(models.Model):
    STATUS_CHOICES=[
         ("general_enquiry","general_enquiry"),
         ("product_support","product_support"),
         ("business","business")
     ]
    full_name=models.CharField(max_length=255)
    email=models.EmailField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="general_enquiry")
    subject=models.CharField(max_length=255)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="CustomerSupport"
        verbose_name_plural="CustomerSupports"

    