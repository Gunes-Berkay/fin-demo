from django.urls import path
from .views import AddPaperToPortfolioView, createPortfolio

urlpatterns = [
    path('api/add-paper/', AddPaperToPortfolioView.as_view(), name='add-paper'),
    path('api/create-portfolio/', createPortfolio.as_view(), name='create-portfolio'),

]
