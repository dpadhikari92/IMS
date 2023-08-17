from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from transactions.models import fgproduction,SaleBill, PurchaseBill,ProductionFG


from django.db.models import Sum

class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        labels = []
        data = []
        production_queryset = (
            fgproduction.objects
            .values('bom__name')  # Group by BOM name
            .annotate(total_production=Sum('quantity'))  # Calculate sum of quantity
            .order_by('-total_production')
        )
        for production in production_queryset:
            labels.append(production['bom__name'])
            data.append(production['total_production'])
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels': labels,
            'data': data,
            'sales': sales,
            'purchases': purchases
        }
        return render(request, self.template_name, context)



class AboutView(TemplateView):
    template_name = "about.html"


def user(request):
    # Your logic here
    context = {
        'user': request.user,
        # Other context variables
    }
    return render(request, 'base.html', context)