from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import Ordering

@shared_task
def delete_old_orders():
    deletion_time = timezone.now() - timedelta(days=1)
    Ordering.objects.filter(ordered_time__lt=deletion_time).delete()
        
        
            