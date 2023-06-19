from django.db import models
from django.shortcuts import render, get_object_or_404

from inventory.models import Stock
from django.utils import timezone
import datetime
from django.db.models import Sum




#contains suppliers
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    gstin = models.CharField(max_length=15, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name


#contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, related_name='purchasesupplier')

    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total


#contains the purchase stocks made
class PurchaseItem(models.Model):   
    billno = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name='purchase_item')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='purchase_items')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)
    supplier_no = models.CharField(default=1,max_length=12)
    freight = models.IntegerField(max_length=50, blank=True, null=True)
    mfg_date = models.DateField(default=datetime.date.today().strftime('%Y-%m-%d'))
    exp_date=models.DateField(default=datetime.date.today().strftime('%Y-%m-%d'))
    purchase_date = models.DateField(default=datetime.date.today().strftime('%Y-%m-%d'))



    def __str__(self):
        return f"Bill no: {self.billno.billno}, Item: {self.stock.name}"

#contains the other details in the purchases bill
class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasedetailsbillno')
    
    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.IntegerField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)    
    cgst = models.FloatField(max_length=50, blank=True, null=True)
    sgst = models.FloatField(max_length=50, blank=True, null=True)
    igst = models.FloatField(max_length=50, blank=True, null=True)    
    freight = models.FloatField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
            # Fetch total from PurchaseItem model
            purchase_items = PurchaseItem.objects.filter(billno=self.billno)
            total_price = purchase_items.aggregate(Sum('totalprice')).get('totalprice__sum', 0)

            # Apply taxes and calculate grand total
            if total_price:
                if self.veh:
                    total_price += self.veh
                cgst = total_price * 0.09
                sgst = total_price * 0.09
                igst = cgst + sgst
                grand_total = total_price + cgst + sgst

                # Assign calculated values to fields
                self.total = str(total_price)
                self.cgst = str(cgst)
                self.sgst = str(sgst)
                self.igst = str(igst)
                self.freight = str(self.veh)
                self.total = str(grand_total)

            super().save(*args, **kwargs)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno)


#contains the sale bills made
class SaleBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    gstin = models.CharField(max_length=15)

    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)
        
    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total

#contains the sale stocks made
class SaleItem(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='saleitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

#contains the other details in the sales bill
class SaleBillDetails(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='saledetailsbillno')
    
    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)


class BOM(models.Model):
    name = models.CharField(max_length=100)
    raw_materials = models.ManyToManyField(Stock, through='BOMRawMaterial')

    def __str__(self):
        return self.name
    
    
class BOMRawMaterial(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        unique_together = ('bom', 'raw_material')

    def __str__(self):
        return f"BOM: {self.bom.name}, Raw Material: {self.raw_material.name}"   
    
    
class Production(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)
    quantity = models.FloatField()
    production_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Production ID: {self.id}, BOM: {self.bom.name}"
    
    
class FGSFG(models.Model):
    name = models.CharField(max_length=100)    
    sfg = models.ForeignKey(Production, on_delete=models.CASCADE)    
    raw_material = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_sfg = models.FloatField()
    quantity_raw = models.FloatField()

  

    def __str__(self):
        return f"FGSFG: {self.name}, SFG: {self.sfg.bom}"   
   
    
    
class ProductionFG(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)    
    quantity_bom = models.FloatField()
    sfg = models.ForeignKey(Production, on_delete=models.CASCADE)
    quantity_sfg = models.FloatField()    
    production_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f" {self.bom}"
    

class Leadtimesfg(models.Model):
    sfg = models.ForeignKey(Production, on_delete=models.CASCADE)     
    Rawcode = models.CharField(max_length=50, blank=True, null=True)
    production_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Production ID: {self.sfg.id}, BOM: {self.sfg.bom}"



class Leadtimefg(models.Model):
    sfg = models.ForeignKey(ProductionFG, on_delete=models.CASCADE)     
    Rawcode = models.CharField(max_length=50, blank=True, null=True)
    production_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Production ID: {self.sfg.id}, BOM: {self.sfg.bom}"
    
        
       

           
    
    
    
   