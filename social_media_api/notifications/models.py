from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        related_name="notifications",
        on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        User,
        related_name="actions",
        on_delete=models.CASCADE
    )

    verb = models.CharField(max_length=255)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("content_type", "object_id")

    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.actor} {self.verb} {self.recipient}"
