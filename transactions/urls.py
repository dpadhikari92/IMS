from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('suppliers/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'), 
    path('purchases/new', views.SelectSupplierView.as_view(), name='select-supplier'), 
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),    
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    
    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new', views.SaleCreateView.as_view(), name='new-sale'),
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),

    path("purchases/<billno>", views.PurchaseBillView.as_view(), name="purchase-bill"),
    path("sales/<billno>", views.SaleBillView.as_view(), name="sale-bill"),
    
    path("bom/", views.create_bom, name="bom"),
    path("bom/list", views.bom_list, name="bom-list"),
    path("bom/details/<int:bom_id>", views.bom_details, name="bom-details"),
    
    path("sfgbom",views.create_sfg_bom,name="sfgbom"),

    path("bomfg/", views.create_productionfg, name="bomfg"),
    path("bomfg/list", views.bom_listFG, name="bomfg-list"),
   
    
    
    
    path("production/", views.produce_item, name="production"), 
    
    path("production/sfg", views.sfg_production_view, name="production-sfg"), 
    path("production/sfgfinal", views.create_sfgfinal, name="production-sfgfinal"),  
    
     
    path("production/list", views.produce_list, name="production-list"),
    path("production/listfg", views.produce_listfg, name="production-listfg"),
    
    path("production/fgsfgbom", views.create_fgsfgbom, name="production-fgsfgbom"),
    path("production/fgsfgbomlist", views.fgsfgbom_list, name="production-fgsfgbomlist"),
    path("production/details/<int:bom_id>", views.bom_detailsfgsfg, name="production-details"),
    
    
    path("production/record", views.leadtimesfg, name="production-record"),  
    path("production/recordfg", views.leadtimefg, name="production-recordfg"),   
    path("production/leadtime", views.leadtimelist, name="production-leadtimelist"),  
    path("production/leadtimefg", views.leadtimelistfg, name="production-leadtimelistfg"),    
]