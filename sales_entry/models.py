from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    USERSTATUS = (
        ('Active', 'Active'),
        ('InActive', 'InActive')
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    is_super_admin = models.BooleanField(default=False, null=True, blank=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    user_status = models.CharField(
        max_length=200, null=True, blank=True, choices=USERSTATUS)
    date_of_joining = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class SalesEntryData(models.Model):
    staff = models.ForeignKey(
        UserProfile, null=True, blank=True,
        on_delete=models.SET_NULL)
    product_name = models.TextField(null=True, blank=True)
    product_quantity = models.CharField(max_length=250, null=True, blank=True)
    product_price = models.CharField(max_length=250, null=True, blank=True)
    payment_type = models.CharField(max_length=250, null=True, blank=True)
    product_image = models.FileField(upload_to='media', null=True, blank=True)
    added_date = models.DateField(auto_now_add=True, null=True, blank=True)
    auto_added_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.product_name) + ' - ' + str(self.added_date)
