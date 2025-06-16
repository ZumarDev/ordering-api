from celery import shared_task
from .models import Ordering


@shared_task
def delete_old_orders(): # TO DO
    pass                
