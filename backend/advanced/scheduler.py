"""
Background scheduler for price alert checks.
Runs every 30 minutes and sends email notifications when prices drop.
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

logger = logging.getLogger(__name__)

_scheduler = None


def check_price_alerts():
    """Check all active price alerts and trigger notifications."""
    try:
        from .models import PriceAlert
        from scrapers import search_all_platforms
        from django.core.mail import send_mail
        from django.conf import settings

        active_alerts = PriceAlert.objects.filter(status='active').select_related('user')
        logger.info(f"Checking {active_alerts.count()} active price alerts...")

        checked_products = {}

        for alert in active_alerts:
            product_key = alert.product_name.lower().strip()

            # Cache scrape results per product to avoid redundant requests
            if product_key not in checked_products:
                try:
                    raw = search_all_platforms(alert.product_name)
                    prices = [
                        float(item['price'])
                        for item in raw
                        if item.get('price') and float(item['price']) > 0
                    ]
                    checked_products[product_key] = min(prices) if prices else None
                except Exception as e:
                    logger.warning(f"Scraping failed for '{alert.product_name}': {e}")
                    checked_products[product_key] = None

            current_price = checked_products[product_key]
            if current_price is None:
                continue

            alert.current_price = current_price
            alert.save(update_fields=['current_price'])

            if current_price <= float(alert.target_price):
                # Trigger the alert
                alert.status = 'triggered'
                alert.save(update_fields=['status', 'current_price'])

                try:
                    send_mail(
                        subject=f'🎉 Price Alert Triggered — {alert.product_name}',
                        message=(
                            f"Great news, {alert.user.get_full_name() or alert.user.email}!\n\n"
                            f"The price of \"{alert.product_name}\" has dropped to ${current_price:.2f}, "
                            f"which is at or below your target price of ${float(alert.target_price):.2f}.\n\n"
                            f"Check it out: {alert.product_url or 'https://localhost:5173'}\n\n"
                            f"— PriceIntel Team"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[alert.user.email],
                        fail_silently=True,
                    )
                    logger.info(f"Alert triggered for user {alert.user.email}: {alert.product_name}")
                except Exception as e:
                    logger.error(f"Failed to send alert email: {e}")

    except Exception as e:
        logger.error(f"Price alert check job failed: {e}")


def start():
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler()
    _scheduler.add_jobstore(DjangoJobStore(), 'default')
    _scheduler.add_job(
        check_price_alerts,
        trigger='interval',
        minutes=30,
        id='check_price_alerts',
        replace_existing=True,
        name='Check Price Alerts',
    )
    _scheduler.start()
    logger.info("APScheduler started — price alert checker running every 30 minutes.")
