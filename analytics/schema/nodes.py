import graphene
from graphene_django.types import DjangoObjectType

from ..models import Analytics

class AnalyticsNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    total_revenue = graphene.String(source='total_revenue')
    monthly_revenue_chart_data = graphene.String(source='monthly_revenue_chart_data')
    total_visits = graphene.Int(source='total_visits')
    monthly_visits_chart_data = graphene.String(source='monthly_visits_chart_data')
    average_order_total = graphene.String(source='average_order_total')

    class Meta:
        model = Analytics
        filter_fields = {
            'store__id': ['exact']
        }
        interfaces = (graphene.relay.Node,)
