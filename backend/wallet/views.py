from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Paper, Portfolio, PortfolioPaper
from .serializers import PortfolioPaperSerializer, PortfolioSerializer

class AddPaperToPortfolioView(APIView):
    def post(self, request):
        portfolio_id = request.data.get('portfolio_id')
        paper_id = request.data.get('paper_id')
        entry_price = request.data.get('entry_price')
        entry_date = request.data.get('entry_date')

        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
            paper = Paper.objects.get(id=paper_id)
        except (Portfolio.DoesNotExist, Paper.DoesNotExist):
            return Response({"error": "Portfolio or Paper not found."}, status=status.HTTP_404_NOT_FOUND)

        portfolio_paper = PortfolioPaper.objects.create(
            portfolio=portfolio,
            paper=paper,
            entry_price=entry_price,
            entry_date=entry_date
        )

        portfolio.papers_list = portfolio.papers_list.add(paper)

        serializer = PortfolioPaperSerializer(portfolio_paper)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class createPortfolio(APIView):
    def post(self, request):
        
        portfolio_name = request.data.get('name')
       
        
        portfolio = Portfolio.objects.create(
            name = portfolio_name
        )

        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


