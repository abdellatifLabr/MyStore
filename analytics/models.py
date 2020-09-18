import datetime
import math
import json

from django.db import models
from django.db.models.signals import post_save
from djmoney.money import Money

from shopping.models import Store


class Analytics(models.Model):
    store = models.OneToOneField('shopping.Store', related_name='analytics', on_delete=models.CASCADE)

    @property
    def total_revenue(self):
        total_revenue = Money(0, 'USD')
        for order in self.store.orders.filter(done=True):
            total_revenue += order.total
        
        return total_revenue

    @property
    def monthly_revenue_chart_data(self):
        months = [datetime.date(2020, i, 20).strftime('%B') for i in range(1, 13)]

        orders = self.store.orders.filter(done=True)
        data = {}

        for order in orders:
            month = months[order.updated.month - 1]

            if month in data:
                data[month] += int(order.total.amount)
            else:
                data[month] = int(order.total.amount)

        return json.dumps({ 'labels': list(data.keys()), 'data': list(data.values()) })
    
    @property
    def total_visits(self):
        return self.store.visits.count()

    @property
    def monthly_visits_chart_data(self):
        months = [datetime.date(2020, i, 20).strftime('%B') for i in range(1, 13)]

        visits = self.store.visits.all()
        data = {}

        for visit in visits:
            month = months[visit.created.month - 1]

            if month in data:
                data[month] += 1
            else:
                data[month] = 1

        return json.dumps({ 'labels': list(data.keys()), 'data': list(data.values()) })
    
    @property
    def average_order_total(self):
        _sum = Money(0, 'USD')
        orders = self.store.orders.filter(done=True)
        for order in orders:
            _sum += order.total
        
        avg = _sum / (orders.count() or 1)
        return avg


def create_analytics(sender, instance, created, **kwargs):
    if created:
        Analytics.objects.create(store=instance)

post_save.connect(create_analytics, sender=Store)
