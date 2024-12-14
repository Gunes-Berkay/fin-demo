from django.db import models

class Paper(models.Model):
    paper_id = models.IntegerField(max_length=100)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    papers_list = models.ManyToManyField('Paper' , through='PortfolioPaper')

    def __str__(self):
        return self.name
    

class PortfolioPaper(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    cur_price = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField()

    def __str__(self):
        return f"{self.paper.name} in {self.portfolio.name}"

