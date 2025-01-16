from rest_framework import serializers
from .models import Paper, Portfolio, PortfolioPaper

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ['paper_id','name']

class PortfolioSerializer(serializers.ModelSerializer):
    
    papers_list = PaperSerializer(many=True)

    class Meta:
         model = Portfolio
         fields = ['portfolio_id','name', 'papers_list']

class PortfolioPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioPaper
        fields = ['portfolio_paper_id','paper', 'portfolio']