from django import apps
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import FileResponse, HttpResponse
import io
from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    FGSFG,
    PurchaseBill, 
    Supplier, 
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
    
   
    
)
from .forms import (
    SelectSupplierForm, 
    PurchaseItemFormset,
    PurchaseDetailsForm, 
    SupplierForm, 
    SaleForm,
    SaleItemFormset,
    SaleDetailsForm,
   
    
)
from inventory.models import Stock
from . import models

from django_filters.views import FilterView
from .filters import BOMFilter





# shows a lists of all suppliers
class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new supplier
class SupplierCreateView(SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier has been created successfully"
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Supplier'
        context["savebtn"] = 'Add Supplier'
        return context     


# used to update a supplier's info
class SupplierUpdateView(SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier details has been updated successfully"
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context


# used to delete a supplier
class SupplierDeleteView(View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Supplier has been deleted successfully"

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object' : supplier})

    def post(self, request, pk):  
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()                                               
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


# used to view a supplier's profile
class SupplierView(View):
    def get(self, request, name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier'  : supplierobj,
            'bills'     : bills
        }
        return render(request, 'suppliers/supplier.html', context)




# shows the list of bills of all purchases 
from django.db.models import Q

class PurchaseView(ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(items__stock__name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

 


# used to select the supplier
class SelectSupplierView(View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})


class PurchaseCreateView(View):
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)
        supplierobj = get_object_or_404(Supplier, pk=pk)
        context = {
            'formset': formset,
            'supplier': supplierobj,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)
        supplierobj = get_object_or_404(Supplier, pk=pk)
        
    

        if formset.is_valid():
            billobj = PurchaseBill(supplier=supplierobj)
            billobj.save()
            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:
                billitem = form.save(commit=False)
                billitem.billno = billobj
                stock = get_object_or_404(Stock, name=billitem.stock.name)
                billitem.totalprice = billitem.perprice * billitem.quantity
                stock.quantity += billitem.quantity
                stock.save()
                billitem.save()
                stock.purchase_items.add(billitem)
            messages.success(request, "Purchased items have been registered successfully")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset': formset,
            'supplier': supplierobj
        }
        return render(request, self.template_name, context)



# used to delete a bill object
class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/transactions/purchases'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, "Purchase bill has been deleted successfully")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)




# shows the list of bills of all sales 
class SaleView(ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to generate a bill object and save items
class SaleCreateView(View):                                                      
    template_name = 'sales/new_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)                          # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form'      : form,
            'formset'   : formset,
            'stocks'    : stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormset(request.POST)                                 # recieves a post method for the formset
        if form.is_valid() and formset.is_valid():
            # saves bill
            billobj = form.save(commit=False)
            billobj.save()     
            # create bill details object
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)      
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity -= billitem.quantity   
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(request, "Sold items have been registered successfully")
            return redirect('sale-bill', billno=billobj.billno)
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        context = {
            'form'      : form,
            'formset'   : formset,
        }
        return render(request, self.template_name, context)


# used to delete a bill object
class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transactions/sales'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Sale bill has been deleted successfully")
        return super(SaleDeleteView, self).delete(*args, **kwargs)




# used to display the purchase bill object
class PurchaseBillView(View):
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        bill = get_object_or_404(PurchaseBill, billno=billno)
        items = PurchaseItem.objects.filter(billno=billno)
        billdetails = get_object_or_404(PurchaseBillDetails, billno=billno)

        context = {
            'bill': bill,
            'items': items,
            'billdetails': billdetails,
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = get_object_or_404(PurchaseBillDetails, billno=billno)
            billdetailsobj.eway = form.cleaned_data['eway']
            billdetailsobj.veh = form.cleaned_data['veh']
            billdetailsobj.destination = form.cleaned_data['destination']
            billdetailsobj.po = form.cleaned_data['po']
            
            # Fetch total from PurchaseItem model
            purchase_items = PurchaseItem.objects.filter(billno=billno)
            total_price = purchase_items.aggregate(Sum('totalprice')).get('totalprice__sum', 0)

            # Apply calculations based on user input and fetched total
            if total_price:
                veh = form.cleaned_data['veh']
                total_price += veh

                cgst = total_price * 0.09
                sgst = total_price * 0.09
                igst = cgst + sgst
                grand_total = total_price + cgst + sgst

                # Assign calculated values to fields
                billdetailsobj.cgst = str(cgst)
                billdetailsobj.sgst = str(sgst)
                billdetailsobj.igst = str(igst)
                billdetailsobj.freight = str(veh)
                billdetailsobj.total = str(grand_total)

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")

        return redirect('purchase-bill', billno=billno)

# used to display the sale bill object
class SaleBillView(View):    
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, billno):
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)
            
            billdetailsobj.eway = request.POST.get("eway")    
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.cgst = request.POST.get("cgst")
            billdetailsobj.sgst = request.POST.get("sgst")
            billdetailsobj.igst = request.POST.get("igst")
            billdetailsobj.cess = request.POST.get("cess")
            billdetailsobj.tcs = request.POST.get("tcs")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)
 

def create_bom(request):
    if request.method == 'POST':
        bom_name = request.POST['name']
        raw_materials = request.POST.getlist('raw_materials[]')
        quantities = request.POST.getlist('quantities[]')

        bom = BOM(name=bom_name)
        bom.save()

        for material, quantity in zip(raw_materials, quantities):
            bom_material = BOMRawMaterial(bom=bom, raw_material_id=material, quantity=quantity)
            bom_material.save()

        messages.success(request, 'BOM saved successfully.')  # Add success message

        return redirect('bom')  # Replace 'bom-list' with the appropriate URL name for the BOM list view

    raw_materials = Stock.objects.all()
    context = {'raw_materials': raw_materials}
    return render(request, 'production/create_bom.html', context)



from django.shortcuts import render, redirect
from .models import Production

def produce_item(request):
    if request.method == 'POST':
        bom_id = request.POST['bom']
        quantity = float(request.POST.get('quantities', 0))  # Convert quantity to float, defaulting to 0 if missing
        
        bom = BOM.objects.get(id=bom_id)
        
        # Check if inventory is sufficient
        raw_materials = bom.raw_materials.all()
        insufficient_inventory = False
        insufficient_raw_materials = []
        for raw_material in raw_materials:
            bom_raw_material = BOMRawMaterial.objects.get(bom=bom, raw_material=raw_material)
            quantity_required = float(bom_raw_material.quantity) * quantity
            
            if raw_material.quantity < quantity_required:
                insufficient_raw_materials.append((raw_material.name, quantity_required))
                insufficient_inventory = True
        
        if insufficient_inventory:
            messages.error(request, 'Insufficient inventory for the following raw materials:')
            for material, required_quantity in insufficient_raw_materials:
                messages.error(request, f'- {material}: {required_quantity}')
            return redirect('production')  # Redirect to production list or desired URL
        
        # Deduct raw materials from inventory
        for raw_material in raw_materials:
            bom_raw_material = BOMRawMaterial.objects.get(bom=bom, raw_material=raw_material)
            quantity_required = float(bom_raw_material.quantity) * quantity
            raw_material.quantity -= quantity_required
            raw_material.save()
        
        # Save production data
        production = Production(bom=bom, quantity=quantity)
        production.save()
        
        # Update the total_qty field based on BOM name
        productions_with_same_bom = Production.objects.filter(bom__name=bom.name)
        total_quantity = productions_with_same_bom.aggregate(Sum('quantity'))['quantity__sum']
        production.total_qty = total_quantity
        production.save()
        
        messages.success(request, 'Order has been placed successfully')
        
        # Generate PDF
        pdf_data = generate_pdf(bom, quantity)
        
        # Return the PDF file as a response
        response = FileResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="production_report.pdf"'
        return response
    
    else:
        boms = BOM.objects.all()
        bom_quantities = {}
        productions = Production.objects.values('bom').annotate(total_quantity=Sum('quantity'))

        for production in productions:
            bom_id = production['bom']
            total_quantity = production['total_quantity']
            bom = BOM.objects.get(id=bom_id)
            
            bom_quantities[bom] = total_quantity
        
        return render(request, 'production/produce_item.html', {'boms': boms, 'bom_quantities': bom_quantities})





def generate_pdf(bom, quantity):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    elements = []

    # Production Details
    production_id = Production.objects.latest('id').id
    product_name = Production.objects.latest('id').bom
    product_quantity = Production.objects.latest('id').quantity
    production_date = Production.objects.latest('id').production_date.strftime('%Y-%m-%d')

    elements.append(Paragraph("Instantina Flavours India Private Limited", styles['Heading1']))
    elements.append(Paragraph("Production Report SFG", styles['Heading1']))
    elements.append(Paragraph(f"Batch No/Production ID: {production_id}", styles['Heading3']))
    elements.append(Paragraph(f"Product Name: {product_name}", styles['Heading3']))
    elements.append(Paragraph(f"Production Quantity: {product_quantity}", styles['Heading3']))
    elements.append(Paragraph(f"Date: {production_date}", styles['Normal']))
    elements.append(Spacer(1, 0.5 * inch))

    # Table Data
    data = [["Raw Material Code", "Raw Material", "Quantity Required (Kg)","RM Batch No","Best Before"]]

    bom_raw_materials = BOMRawMaterial.objects.filter(bom=bom)
    for bom_raw_material in bom_raw_materials:      
        quantity_required = round(bom_raw_material.quantity * quantity, 5)

        stock = bom_raw_material.raw_material
        data.append([stock.item_code, stock.name, str(quantity_required)])

    # Table Style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
    ])

    table = Table(data, colWidths=[150, 150, 150,100,100])
    table.setStyle(table_style)
    elements.append(table)

    doc.build(elements)

    buffer.seek(0)
    return buffer



    

from django.db.models import Q




from django.shortcuts import get_object_or_404

def bom_list(request):
    query = request.GET.get('query')
    boms = BOM.objects.all()
    
    if query:
        boms = boms.filter(name__icontains=query)
    
    context = {'boms': boms, 'query': query}
    return render(request, 'production/bom_list.html', context)




def bom_listFG(request):
    query = request.GET.get('query')
    bom_raw_materials = FGSFG.objects.all()
    
    if query:
        bom_raw_materials = bom_raw_materials.filter(bom__name__icontains=query)
    
    paginator = Paginator(bom_raw_materials, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'bom_raw_materials': page_obj, 'query': query}
    return render(request, 'production/bom_listfg.html', context)  


from django.db.models import Max

def produce_list(request):
    query = request.GET.get('query')
    productions = Production.objects.all()
    
    if query:
        productions = productions.filter(bom__name__icontains=query)
    
    productions = productions.values('bom__name').annotate(latest_total_qty=Max('total_qty'))
    
    context = {'productions': productions, 'query': query}
    return render(request, 'production/production_list.html', context)



def create_productionfg(request):
    if request.method == 'POST':
        bom_id = request.POST['bom']
        sfg_name = request.POST['sfg']
        quantity_bom = float(request.POST.get('quantity_bom', 0))
        quantity_sfg = float(request.POST.get('quantity_sfg', 0))

        bom = BOM.objects.get(id=bom_id)
        sfg = Production.objects.filter(bom__name=sfg_name).first()

        if sfg is None:
            messages.error(request, f'Production with name "{sfg_name}" does not exist')
            return redirect('bomfg')

        # Check if inventory is sufficient for BOM
        raw_materials = bom.raw_materials.all()
        insufficient_inventory = False
        insufficient_raw_materials = []
        for raw_material in raw_materials:
            bom_raw_material = BOMRawMaterial.objects.get(bom=bom, raw_material=raw_material)
            quantity_required = float(bom_raw_material.quantity) * quantity_bom

            if raw_material.quantity < quantity_required:
                insufficient_raw_materials.append((raw_material.name, quantity_required))
                insufficient_inventory = True

        if insufficient_inventory:
            messages.error(request, 'Insufficient inventory for the following raw materials:')
            for material, required_quantity in insufficient_raw_materials:
                messages.error(request, f'- {material}: {required_quantity}')
            return redirect('bomfg')

        # Deduct raw materials from inventory for BOM
        for raw_material in raw_materials:
            bom_raw_material = BOMRawMaterial.objects.get(bom=bom, raw_material=raw_material)
            quantity_required = float(bom_raw_material.quantity) * quantity_bom
            raw_material.quantity -= quantity_required
            raw_material.save()

        # Check if SFG quantity is available
        if sfg.total_qty < quantity_sfg:
            messages.error(request, 'Insufficient SFG quantity')
            return redirect('bomfg')

        # Deduct quantity from SFG
        sfg.total_qty -= quantity_sfg
        sfg.save()
        
        # Update the total quantity of SFG
        sfg.update_total_qty()

        # Save production data
        production = ProductionFG(bom=bom, quantity_bom=quantity_bom, sfg=sfg, quantity_sfg=quantity_sfg)
        production.save()

        messages.success(request, 'Order has been placed successfully')

        # Generate PDF
        pdf_data = generate_pdffg(bom, quantity_bom, quantity_sfg)

        # Return the PDF file as a response
        response = FileResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="production_report.pdf"'
        return response

    else:
        boms = BOM.objects.all()
        sfgs = Production.objects.values('bom__name').distinct()

        return render(request, 'production/create_bomFG.html', {'boms': boms, 'sfgs': sfgs})



    

def generate_pdffg(bom, quantity_bom, quantity_sfg):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    elements = []

    # Production Details
    productionfg = ProductionFG.objects.filter(bom=bom).latest('id')
    production_id = productionfg.id
    product_name = productionfg.bom
    product_name = productionfg.bom
    product_quantity = productionfg.quantity_bom
    production_date = productionfg.production_date.strftime('%Y-%m-%d')

    elements.append(Paragraph("Instantina Flavours India Private Limited", styles['Heading1']))
    elements.append(Paragraph("Production Report FG", styles['Heading1']))
    elements.append(Paragraph(f"Production ID: {production_id}", styles['Heading3']))
    elements.append(Paragraph(f"Product Name: {product_name}", styles['Heading3']))
    elements.append(Paragraph(f"Production Quantity: {product_quantity}", styles['Heading3']))
    elements.append(Paragraph(f"Date: {production_date}", styles['Normal']))
    elements.append(Spacer(1, 0.8 * inch))

    # Table Data
    data = [["RM Code","Raw Material", "Qty (Kg)", "SFG Name", "SFG Quantity (Kg)","RM Batch no","SFG Id","Completion date",]]

    raw_materials = bom.raw_materials.all()
    for raw_material in raw_materials:
        bom_raw_material = BOMRawMaterial.objects.get(bom=bom, raw_material=raw_material)
        quantity_required = round(float(bom_raw_material.quantity) * quantity_bom, 5)

        sfg_name = productionfg.sfg.bom if productionfg.sfg else ""  # Assuming SFG has a 'name' attribute
        sfg_quantity = productionfg.quantity_sfg if productionfg.sfg else 0
        stock=bom_raw_material.raw_material
        data.append([stock.item_code,raw_material.name, str(quantity_required), sfg_name, str(sfg_quantity)])

    # Table Style
    table_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
    ])

    table = Table(data, colWidths=[80, 150, 80,120,80,80,80,100])
    table.setStyle(table_style)
    elements.append(table)

    doc.build(elements)

    buffer.seek(0)
    return buffer


def produce_listfg(request):
    query = request.GET.get('query')
    leadtimes = Leadtimefg.objects.all()

    if query:
        leadtimes = leadtimes.filter(sfg__bom__name__icontains=query)

    paginator = Paginator(leadtimes, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'leadtimes': page_obj, 'query': query}
    return render(request, 'production/produce_listfg.html', context)



def leadtimesfg(request):
    if request.method == 'POST':
        sfg_id = request.POST.get('sfg')
        rawcode = request.POST.get('rawcode')

        # Check if the SFG already has a Rawcode associated with it
        existing_leadtime = Leadtimesfg.objects.filter(sfg_id=sfg_id, Rawcode__isnull=False).first()
        if existing_leadtime:
            error_message = f"Rawcode already exists for SFG ID: {sfg_id}"
            # You can choose to display this error message in the template
            return render(request, 'production/leadtimesfg.html', {'error_message': error_message})

        # Create a new Leadtimesfg object
        new_leadtime = Leadtimesfg(sfg_id=sfg_id, Rawcode=rawcode)
        new_leadtime.save()

        # Redirect to a success page or display a success message
        return redirect('production-record')

    # If the request method is GET, retrieve the available SFGs
    sfg_list = Production.objects.filter(leadtimesfg__isnull=True)
    return render(request, 'production/leadtimesfg.html', {'sfg_list': sfg_list})

def leadtimelist(request):
    query = request.GET.get('query')
    leadtimes = Leadtimesfg.objects.all()

    if query:
        leadtimes = leadtimes.filter(sfg__bom__name__icontains=query)

    paginator = Paginator(leadtimes, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'leadtimes': page_obj, 'query': query}
    return render(request, 'production/leadtimelist.html', context)



def leadtimefg(request):
    if request.method == 'POST':
        sfg_id = request.POST.get('sfg')
        rawcode = request.POST.get('rawcode')

        # Check if the SFG already has a Rawcode associated with it
        existing_leadtime = Leadtimefg.objects.filter(sfg_id=sfg_id, Rawcode__isnull=False).first()
        if existing_leadtime:
            error_message = f"Rawcode already exists for SFG ID: {sfg_id}"
            # You can choose to display this error message in the template
            return render(request, 'production/leadtimesfg.html', {'error_message': error_message})

        # Create a new Leadtimesfg object
        new_leadtime = Leadtimefg(sfg_id=sfg_id, Rawcode=rawcode)
        new_leadtime.save()

        # Redirect to a success page or display a success message
        return redirect('production-record')

    # If the request method is GET, retrieve the available SFGs
    sfg_list = ProductionFG.objects.filter(leadtimefg__isnull=True)
    return render(request, 'production/leadtimefg.html', {'sfg_list': sfg_list})

def leadtimelistfg(request):
    query = request.GET.get('query')
    leadtimes = Leadtimefg.objects.all()

    if query:
        leadtimes = leadtimes.filter(sfg__bom__name__icontains=query)

    paginator = Paginator(leadtimes, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'leadtimes': page_obj, 'query': query}
    return render(request, 'production/leadtimelistfg.html', context)



def bom_details(request, bom_id):
    bom = get_object_or_404(BOM, pk=bom_id)
    bom_raw_materials = bom.bomrawmaterial_set.all()
    context = {'bom': bom, 'bom_raw_materials': bom_raw_materials}
    return render(request, 'production/bom_details.html', context)