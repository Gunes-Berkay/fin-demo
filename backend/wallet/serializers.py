from rest_framework import serializers
from .models import Paper, Portfolio, PortfolioPaper

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ['id', 'name']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
         model = Portfolio
         fields = ['name', 'papers_list']

class PortfolioPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioPaper
        fields = ['paper', 'portfolio', 'entry_price', 'cur_price' ,'number', 'entry_date']