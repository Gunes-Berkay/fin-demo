from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Paper, Portfolio, PortfolioPaper
from .serializers import PortfolioPaperSerializer, PortfolioSerializer, PaperSerializer, TransactionsSerializer
from .models import Portfolio
from django.db import transaction
from django.db import connections
from django.http import JsonResponse

class AddPaperToPortfolioView(APIView):
    def post(self, request):
        portfolio_id = request.data.get('portfolio_id')
        paper_name = request.data.get('paper_name')
        #entry_price = request.data.get('entry_price')
        #entry_date = request.data.get('entry_date')

        try:
            portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
            paper = Paper.objects.get(name=paper_name)
        except (Portfolio.DoesNotExist, Paper.DoesNotExist):
            return Response({"error": "Portfolio or Paper not found."}, status=status.HTTP_404_NOT_FOUND)

        portfolio_paper = PortfolioPaper.objects.create(
            portfolio=portfolio,
            paper=paper,
            #entry_price=entry_price,
            #entry_date=entry_date
        )

        portfolio.papers_list.add(paper)

        serializer = PortfolioPaperSerializer(portfolio_paper)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class createPortfolio(APIView):
    def post(self, request):
        portfolio_name = request.data.get('name')
        papers_data = request.data.get('papers', [])  

       
        try:
            with transaction.atomic():
                
                portfolio = Portfolio.objects.create(name=portfolio_name)

                # Papers (hisseler) portföye eklenir
                for paper_id in papers_data:
                    try:
                        paper = Paper.objects.get(id=paper_id)  # Her bir paper_id için Paper modelinden obje alınır
                        portfolio.papers_list.add(paper)  # Portfolio'nun papers_list alanına eklenir
                    except Paper.DoesNotExist:
                        return Response(
                            {"error": f"Paper with ID {paper_id} not found."},
                            status=status.HTTP_404_NOT_FOUND
                        )
                
                # Transaction başarıyla tamamlandıktan sonra
                serializer = PortfolioSerializer(portfolio)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Eğer bir hata oluşursa transaction rollback yapılır
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


    
class portfolioListView(APIView):
    def get(self, request):
        portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PaperListView(APIView):
    def get(self, request):
        papers = Paper.objects.using('papers_db').all()
        serializer = PaperSerializer(papers, many=True)
        return Response(serializer.data)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Transactions, Portfolio, Paper

class TransactionCreateView(APIView):
    def post(self, request):
        serializer = TransactionsSerializer(data=request.data)
        if serializer.is_valid():
            portfolio_id = serializer.validated_data['portfolio'].portfolio_id
            paper_id = serializer.validated_data['paper'].id
            entry_price = serializer.validated_data['entry_price']
            quantity = serializer.validated_data['quantity']
            buy = serializer.validated_data['buy']
            
            # Burada yeni transaction ekliyoruz
            transaction = Transactions.objects.create(
                portfolio_id=portfolio_id,
                paper_id=paper_id,
                entry_price=entry_price,
                quantity=quantity,
                buy=buy
            )
            return Response(TransactionsSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePortfolioPaper(APIView):
    def put(self, request, portfolio_paper_id):
        try:
            portfolio_paper = PortfolioPaper.objects.get(portfolio_paper_id=portfolio_paper_id)
            serializer = PortfolioPaperSerializer(portfolio_paper, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except PortfolioPaper.DoesNotExist:
            return Response({"error": "PortfolioPaper not found"}, status=404)

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Paper
import requests

class UpdatePaperPrices(APIView):
    def get(self, request):
        # Örnek: API'den fiyatları alıyoruz
        response = requests.get('https://api.example.com/get_paper_prices')
        paper_prices = response.json()

        # Veritabanındaki her Paper'ın fiyatını güncelliyoruz
        for paper in paper_prices:
            try:
                paper_obj = Paper.objects.using('papers_db').get(symbol=paper['symbol'])
                paper_obj.max_supply = paper['max_supply']
                paper_obj.circulating_supply = paper['circulating_supply']
                paper_obj.total_supply = paper['total_supply']
                paper_obj.inifinite_supply = paper['inifinite_supply']
                paper_obj.cmc_rank = paper['cmc_rank']
                paper_obj.save()
            except Paper.DoesNotExist:
                continue  # Paper bulunamadıysa geçiyoruz

        return Response({"message": "Prices updated successfully"})

def get_papers(request):
    with connections['papers_db'].cursor() as cursor:
        cursor.execute("SELECT id,symbol,name FROM CMC_INFO")
        rows = cursor.fetchall()

    papers = [{"id": row[0],"symbol":row[1] ,"name": row[2]} for row in rows]
    return JsonResponse(papers, status=200, safe=False)
