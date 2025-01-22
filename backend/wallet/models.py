from django.db import models

class Portfolio(models.Model):
    portfolio_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    papers_list = models.ManyToManyField('Paper', through='PortfolioPaper')

    class Meta:
        db_table = 'wallet_portfolio'  # Belirli tablo ismini burada tanımlayın

    def __str__(self):
        return self.name


class Paper(models.Model):
    paper_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'wallet_paper'  

    def __str__(self):
        return self.name

    

class PortfolioPaper(models.Model):
    portfolio_paper_id = models.AutoField(primary_key=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'wallet_portfolio_paper'

    def __str__(self):
        return f"{self.paper.name} in {self.portfolio.name}"

