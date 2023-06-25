from django.db import models
 
   
class Stock(models.Model):
    item_code =models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, unique=True)
    quantity = models.FloatField(default=0)
    hsn=models.IntegerField(default=0)
    cas=models.CharField(max_length=30,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name