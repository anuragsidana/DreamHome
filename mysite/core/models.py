from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    # ADMIN_CHOICE = (("YES", True), ("NO", False))
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

#signal when user created then also create profile object
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Customer(models.Model):
    agent=models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200,blank=True)
    # father_name=models.CharField(max_length=200)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    #                              message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    # permanent_address=models.CharField(max_length=500)
    # aadhar_regx= RegexValidator(regex= r'^\d{12}$',message='aadhar must be of 121 digits')
    # aadhar_no= models.CharField(validators=[aadhar_regx],max_length=12)
    # # whenever a new Cutomer created redirect it to its details page
    def get_absolute_url(self):
        # detail view need primary key argument , hence to get primary key of the self object we wrote kwargs
        return reverse('customer_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.first_name

class Docs(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    doc_type=models.CharField(max_length=200)

    # whenever a new Document created redirect it to its details page
    def get_absolute_url(self):
        # detail view need primary key argument , hence to get primary key of the self object we wrote kwargs
        return reverse('document_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.doc_type

