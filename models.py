from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    week_number = models.CharField(max_length=2, blank=True, editable=False)
    end_date = models.DateField()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        # Calculate the ISO week number and set it if blank
        if not self.week_number:
            self.week_number = str(self.start_date.isocalendar()[1])
        super().save(*args, **kwargs)


class Investment(models.Model):
    ACTION_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    shares = models.IntegerField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES, default='buy')

    def save(self, *args, **kwargs):
        # Calculate total_value when saving
        self.total_value = self.shares * self.current_price
        super().save(*args, **kwargs)


    def process_payment(self):
        """ Simulate the payment process. Mark payment as processed. """
        # Here you'd implement actual payment logic, e.g., interacting with a payment gateway.
        self.payment_status = True  # For now, just simulate it as processed.

    def __str__(self):
        return f"{self.action.capitalize()} {self.shares} shares of {self.ticker} at {self.current_price}"
