from django.db import models
from django.conf import settings


class PriceAlert(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('triggered', 'Triggered'),
        ('paused', 'Paused'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='price_alerts')
    product_name = models.CharField(max_length=255, db_index=True)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_url = models.URLField(max_length=2048, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} — {self.product_name} @ {self.target_price}"


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=512, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.email}: {self.query}"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product_name = models.CharField(max_length=255, db_index=True)
    store = models.CharField(max_length=100, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_url = models.URLField(max_length=2048, blank=True, default='')
    image_url = models.URLField(max_length=2048, blank=True, default='')
    added_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-added_at']
        unique_together = ('user', 'product_url')

    def __str__(self):
        return f"{self.user.email} — {self.product_name}"


class PriceHistory(models.Model):
    product_name = models.CharField(max_length=255, db_index=True)
    store = models.CharField(max_length=100, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.product_name} @ {self.price} ({self.timestamp.date()})"
