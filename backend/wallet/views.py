from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Paper, Portfolio, PortfolioPaper
from .serializers import PortfolioPaperSerializer, PortfolioSerializer, PaperSerializer
from .models import Portfolio
from django.db import transaction


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
    
# class createPortfolio(APIView):
#     def post(self, request):
#         portfolio_name = request.data.get('name')
#         papers_data = request.data.get('papers', [])  # Gelen istekten papers listesi alınır (varsayılan boş liste)

#         # Yeni bir Portfolio oluşturulur
#         portfolio = Portfolio.objects.create(
#             name=portfolio_name
#         )

#         # Papers (hisseler) portföye eklenir
#         for paper_id in papers_data:
#             try:
#                 paper = Paper.objects.get(id=paper_id)  # Her bir paper_id için Paper modelinden obje alınır
#                 portfolio.papers_list.add(paper)  # Portfolio'nun papers_list alanına eklenir
#             except Paper.DoesNotExist:
#                 return Response(
#                     {"error": f"Paper with ID {paper_id} not found."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#         # Son olarak portföyün serializer'ı hazırlanır ve cevap döndürülür
#         serializer = PortfolioSerializer(portfolio)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)




class createPortfolio(APIView):
    def post(self, request):
        portfolio_name = request.data.get('name')
        papers_data = request.data.get('papers', [])  # Gelen istekten papers listesi alınır (varsayılan boş liste)

        # Bir transaction başlatıyoruz
        try:
            with transaction.atomic():
                # Yeni bir Portfolio oluşturulur
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
    
class paperListView(APIView):
    def get(self, request):
        papers = Paper.objects.all()
        serializer = PaperSerializer(papers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

