from django.db import models
from accounts.models import CustomUser

# Create your models here.


class Owner(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    farming_name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    def __str__(self):
        return self.user.first_name + " " + self.farming_name
    


class Product(models.Model):
    owner=models.ForeignKey(Owner,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField()
    product_image=models.ImageField(upload_to='product_images')


    def __str__(self):
        return self.product_name



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in {self.cart.user.username}'s cart"




class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"
    



class ProductMessage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} about {self.product.product_name}"
    




class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.product_name}"