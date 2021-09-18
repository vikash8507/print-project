from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

from main.models import Voter

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(post_delete, sender=Voter)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes thumbnail files on `post_delete` """
    if instance.photo:
        _delete_file(instance.photo.path)
    if instance.barcode:
        _delete_file(instance.barcode.path)