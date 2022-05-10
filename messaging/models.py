from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    TYPES = [
        ('Offer_accepted', 'Offer Accepted'),
        ('Offer_rejected', 'Offer Rejected'),
        ('Offer_new', 'New Offer'),
        ('Sale_completed', 'Sale Completed'),
        ('Item_inquiry', 'Item inquiry'),
        ('Message', 'Message'),
    ]
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    subject = models.CharField(max_length=191)
    body = models.TextField()
    related_content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, blank=True, null=True)
    related_object_id = models.PositiveBigIntegerField(blank=True, null=True)
    related = GenericForeignKey('related_content_type', 'related_object_id')
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    type = models.CharField(
        max_length=14,
        choices=TYPES,
        default='Message',
    )
