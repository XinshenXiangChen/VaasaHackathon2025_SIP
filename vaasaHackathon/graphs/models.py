from django.db import models

# Create your models here.
class Proces(models.Model):
    lci_number = models.IntegerField(primary_key=True)
    unit = models.TextField()
    process_name = models.TextField()
    carbon_dioxide = models.IntegerField()
    total_eco_costs = models.IntegerField()
    eco_costs_e1 = models.IntegerField()
    eco_costs_e2 = models.IntegerField()
    eco_costs_e3 = models.IntegerField()
    eco_costs_e4 = models.IntegerField()
    eco_costs_e5 = models.IntegerField()
 
