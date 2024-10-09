from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Login(AbstractUser):
    userType = models.CharField(max_length=50, choices=[('user', 'User'), ('promoter', 'Promoter')], default='user')
    viewpassword=models.CharField(max_length=50)
    
    def _str_(self):
        return self.username

class UserRegister(models.Model):
    
    user=models.OneToOneField(Login,on_delete=models.CASCADE,null=True)
    user_fullname=models.CharField(max_length=100)
    user_email=models.EmailField()
    user_username=models.TextField()
    user_language = models.CharField(max_length=50,default='English', choices=[
        ('Malayalam', 'Malayalam'),
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Tamil', 'Tamil'),
    ])
    redeem_code = models.CharField(max_length=100, blank=True, null=True)
    user_password=models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    enrolled=models.BooleanField(default=False)
    whatsapp=models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True,null=True)

    amountpaid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    howmuchperuser = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=50.00)

    def __str__(self):
        return f"{self.user_username}"

class AdminMessage(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]} - {self.timestamp}"
    
class DayTasks(models.Model):
    title=models.CharField(max_length=50)
    Quotefortask=models.TextField(max_length=100)
    imagefortask=models.ImageField(upload_to='imagefortask/')
    topic=models.CharField(max_length=50,null=True)
    timeduration=models.TextField(null=True)
    headingforexercise=models.TextField(null=True)
    exercise1=models.TextField(null=True)
    exercise1ans=models.CharField(max_length=50,null=True)
    exercise2=models.TextField(null=True)
    exercise2ans=models.CharField(max_length=50,null=True)
    exercise3=models.TextField(null=True)
    exercise3ans=models.CharField(max_length=50,null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class UserTaskStatus(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    task = models.ForeignKey(DayTasks, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'task')
    
    def __str__(self):
        return f"{self.user.user_username} - {self.task.title}"
    
class ProgressBar(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, null=True)
    percentage=models.IntegerField()
    updated_time = models.DateTimeField(auto_now_add=True)

class Courseredirect(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, null=True)
    clicked=models.BooleanField(default=False)

class Usermessage(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()
    replied=models.BooleanField(default=False)
    message_recieved = models.DateTimeField(auto_now_add=True)

class groupLink(models.Model):
    link=models.TextField()

class Review(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_fullname}'s with {self.rating} reviews"
    
class PaymentPrice(models.Model):
    amount=models.IntegerField(null=True)
    payment_QRCODE = models.ImageField(upload_to='payment_QRCODE/', blank=True, null=True)
    offer_payment_QRCODE = models.ImageField(upload_to='offer_payment_QRCODE/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class Promoterpayment(models.Model):
    user= models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    requested= models.BooleanField(default=False)
    amount=models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, null=True)