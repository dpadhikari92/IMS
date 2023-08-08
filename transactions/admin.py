from django.contrib import admin
from .models import (
    Supplier, 
    PurchaseBill, 
    PurchaseItem,
    PurchaseBillDetails, 
    SaleBill, 
    SaleItem,
    SaleBillDetails,
    BOM,
    BOMRawMaterial,
    Production,  
    FGSFG,
    ProductionFG,
    Leadtimesfg,
    Leadtimefg,
    SfgBom,
    sfgproduction,
    Sfgfinal,
    FGSFGNEW,
    fgproduction,
    RawMaterialEntry,
    MultipleSFG,

    
    
    
)

admin.site.register(Supplier)
admin.site.register(BOM)
admin.site.register(BOMRawMaterial)
admin.site.register(Production)
admin.site.register(PurchaseBill)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseBillDetails)
admin.site.register(SaleBill)
admin.site.register(SaleItem)
admin.site.register(SaleBillDetails)
admin.site.register(Leadtimesfg)
admin.site.register(FGSFG)
admin.site.register(SfgBom)
admin.site.register(Sfgfinal)
admin.site.register(sfgproduction)
admin.site.register(ProductionFG)
admin.site.register( Leadtimefg)
admin.site.register(fgproduction)
admin.site.register(RawMaterialEntry)
admin.site.register( FGSFGNEW)
admin.site.register(MultipleSFG)


