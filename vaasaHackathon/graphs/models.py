from django.db import models

# Create your models here.
class Proces(models.Model):
    lci_number = models.TextField(primary_key=True)
    unit = models.TextField()
    process_name = models.TextField()
    carbon_dioxide = models.FloatField()
    total_eco_costs = models.FloatField()
    eco_costs_e1 = models.FloatField()
    eco_costs_e2 = models.FloatField()
    eco_costs_e3 = models.FloatField()
    eco_costs_e4 = models.FloatField()
    eco_costs_e5 = models.FloatField()

class UploadedData(models.Model):
    name = models.TextField()
    category = models.TextField()
    quantity = models.FloatField()
    unit = models.TextField()
    carbon_dioxide = models.FloatField()
    total_eco_costs = models.FloatField()
    eco_costs_e1 = models.FloatField()
    eco_costs_e2 = models.FloatField()
    eco_costs_e3 = models.FloatField()
    eco_costs_e4 = models.FloatField()
    eco_costs_e5 = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'uploaded_data'
 
