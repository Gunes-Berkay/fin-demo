from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transactions, PortfolioPaper

@receiver(post_save, sender=Transactions)
def update_portfolio_paper(sender, instance, **kwargs):
    portfolio_paper, created = PortfolioPaper.objects.get_or_create(
        portfolio=instance.portfolio, 
        paper=instance.paper
    )
    
    # Alım işlemi ise adeti artır, satım ise azalt
    portfolio_paper.total_quantity += instance.quantity  
    portfolio_paper.save()
