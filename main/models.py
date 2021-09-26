from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Voter(models.Model):
    epic = models.CharField(max_length=20)
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    blck1 = models.CharField(max_length=100)
    blck2 = models.CharField(max_length=100, default="")
    subblock = models.CharField(max_length=100)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=100)
    birth = models.DateField(null=True, blank=True)
    gname1 = models.CharField(max_length=100)
    gname2 = models.CharField(max_length=100)
    partno = models.CharField(max_length=100)
    partname1 = models.CharField(max_length=100)
    partname2 = models.CharField(max_length=100, default="")
    serialno = models.CharField(max_length=100)
    guardian_title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', default="voter.png")
    barcode = models.ImageField(upload_to='barcodes/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.epic


class Payment(models.Model):
    razorpay_order_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username) + "->" + str(self.razorpay_order_id)


class PANCard(models.Model):
    pan = models.CharField(max_length=15)
    name = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)
    birth = models.DateField()
    photo = models.ImageField(upload_to="pan/photos/")
    sign = models.ImageField(upload_to="pan/signs/")
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name + self.pan