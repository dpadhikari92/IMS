from decimal import ROUND_HALF_UP, Decimal
from django.db import models
from django.shortcuts import render, get_object_or_404

from inventory.models import Stock
from django.utils import timezone
import datetime
from django.db.models import Sum

from django.db import transaction





#contains suppliers
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254,  blank=True, null=True)
    gstin = models.CharField(max_length=15, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name


#contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, related_name='purchasesupplier')
    

    def __str__(self):
	    return "Bill no: " + str(self.billno)
 
    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)
    
    def get_items(self):
        return PurchaseBillDetails.objects.filter(billno=self)

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
    exp = models.DateField(default=datetime.date.today)  # Add the exp field
    mfg = models.DateField(default=datetime.date.today)  # Add the mfg field
    receipt_date = models.DateField(default=datetime.date.today)
    quantity = models.FloatField(default=1.0)
    perprice = models.FloatField(default=1)
    totalprice = models.IntegerField(default=1)
    coa = models.CharField(max_length=50, blank=True, null=True)
    supplier_no = models.CharField(max_length=50, blank=True, null=True)
    
    purchase_code = models.CharField(max_length=100, blank=True, null=True)
    
    
    def __str__(self):
        return f"Bill no: {self.billno.billno}, Item: {self.stock.name}"
    
    
    def generate_code_purchase(self):
        purchase_code = self.stock.item_code
        purchase_count = PurchaseItem.objects.filter(stock=self.stock).count() + 1
        self.purchase_code = f"{purchase_code}/{purchase_count}"
        self.save()

    def save(self, *args, **kwargs):
        if not self.purchase_code:
            self.generate_code_purchase()
        super().save(*args, **kwargs)
    
    
        
        

#contains the other details in the purchases bill
class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasedetailsbillno')      
    sup_invoice_no=models.FloatField(max_length=50, blank=True, null=True)
    mfg=models.CharField(max_length=50, blank=True, null=True)    
    exp=models.CharField(max_length=50, blank=True, null=True)
    receipt_date=models.CharField(max_length=50, blank=True, null=True)
    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.FloatField(max_length=50, blank=False,null=True)
    invoice = models.DateField(default=datetime.date.today().strftime('%Y-%m-%d'))
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

                # Round the calculated values to 2 decimal places
                cgst = round(cgst, 2)
                sgst = round(sgst, 2)
                igst = round(igst, 2)
                grand_total = round(grand_total)  # Round off to the nearest whole number

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
    code = models.CharField(max_length=100)
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
    production_date = models.DateField(default=datetime.date.today().strftime('%Y-%m-%d'))
    total_qty = models.FloatField(default=0)    
    code_sfg = models.CharField(max_length=100, blank=True, null=True)
    
    
    def __str__(self):
        return f"Production ID: {self.id}, BOM: {self.bom.name}"
    
    def update_total_qty(self):
        if self.total_qty is None:
            self.total_qty = 0
        self.total_qty += self.quantity
        self.save()
        
        
    def generate_code_sfg(self):
        bom_code = self.bom.code
        production_count = Production.objects.filter(bom=self.bom).count() + 1
        self.code_sfg = f"{bom_code}/{production_count}"
        self.save()

    def save(self, *args, **kwargs):
        if not self.code_sfg:
            self.generate_code_sfg()
        super().save(*args, **kwargs)
  
  
  
class ProductionFG(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)    
    quantity_bom = models.FloatField()
    sfg = models.ForeignKey(Production, on_delete=models.CASCADE)
    quantity_sfg = models.FloatField()    
    production_date = models.DateField(auto_now_add=True)
    code_fg = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f" {self.bom} - {self.sfg.bom.name}"
    
    
    def generate_code_fg(self):
        bom_code = self.bom.code
        production_count = ProductionFG.objects.filter(bom=self.bom).count() + 1
        self.code_fg = f"{bom_code}/{production_count}"
        self.save()

    def save(self, *args, **kwargs):
        if not self.code_fg:
            self.generate_code_fg()
        super().save(*args, **kwargs)
        
        
        
    

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
    
        
       
 
class SfgBom(models.Model):   
    sfg = models.ForeignKey(Production, on_delete=models.CASCADE)
    quantity_sfg = models.FloatField()   
    
    def __str__(self):
        return f" {self.sfg.bom.name}"
     
     
class Sfgfinal(models.Model):
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)
    sfg = models.ForeignKey(SfgBom, on_delete=models.CASCADE)
    
    def __str__(self):
        return f" {self.bom.name} -"

    
class FGSFG(models.Model):
    name = models.CharField(max_length=100) 
    code = models.CharField(max_length=100)    
    sfg = models.ForeignKey(Production, on_delete=models.CASCADE) 
    raw_material = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_sfg = models.FloatField()
    quantity_raw = models.FloatField()  

    def __str__(self):
        return f"FGSFG: {self.name}, {self.code}"      
    
    


class FGSFGNEW(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)    
    sfg = models.ManyToManyField(BOM, through='MultipleSFG')
    production = models.ForeignKey(Production, on_delete=models.CASCADE, null=True, blank=True)
    raw_materials = models.ManyToManyField(Stock, through='RawMaterialEntry')
    
    

    def __str__(self):
        return f"FGSFGNEW: {self.name}, SFG: {self.sfg}, Raw Material: {', '.join(str(raw_material) for raw_material in self.raw_materials.all())}"


class MultipleSFG(models.Model):
    fgsfgnew = models.ForeignKey(FGSFGNEW, on_delete=models.CASCADE)
    sfg = models.ForeignKey(BOM, on_delete=models.CASCADE)
    quantity_sfg = models.FloatField()    
    
    def __str__(self):
        return f"MultipleSFG: {self.sfg}, Quantity: {self.quantity_sfg}"
    

class RawMaterialEntry(models.Model):
    fgsfgnew = models.ForeignKey(FGSFGNEW, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_raw = models.FloatField()

    def __str__(self):
        return f"Raw Material Entry: {self.raw_material}, Quantity: {self.quantity_raw}"


    
class sfgproduction(models.Model):
    bom = models.ForeignKey(FGSFG, on_delete=models.CASCADE)    
    quantity= models.FloatField()   
    production_date = models.DateField(auto_now_add=True)    

    def __str__(self):
        return f" {self.bom} "
    
    

class fgproduction(models.Model):
    bom = models.ForeignKey(FGSFGNEW, on_delete=models.CASCADE) 
    production = models.ForeignKey(Production, on_delete=models.CASCADE, null=True, blank=True)   
    quantity= models.FloatField()   
    code_fg = models.CharField(max_length=100, blank=True, null=True)
    production_date = models.DateField(default=datetime.date.today().strftime('%Y-%m-%d'))

    def __str__(self):
        return f" {self.bom.name} "
    
    
    
    def generate_code_fg(self):
        bom_code = self.bom.code
        production_count = fgproduction.objects.filter(bom=self.bom).count() + 1
        self.code_fg = f"{bom_code}/{production_count}"
        self.save()

    def save(self, *args, **kwargs):
        if not self.code_fg:
            self.generate_code_fg()
        super().save(*args, **kwargs)
    
    

