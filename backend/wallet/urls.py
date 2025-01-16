from django.urls import path
from .views import AddPaperToPortfolioView, createPortfolio, portfolioListView, paperListView

urlpatterns = [
    path('api/add-paper/', AddPaperToPortfolioView.as_view(), name='add-paper'),
    path('api/create-portfolio/', createPortfolio.as_view(), name='create-portfolio'),
    path('api/portfolios/', portfolioListView.as_view(), name='portfolio-list'),
    path('api/papers/', paperListView.as_view(), name='papers'),


]
