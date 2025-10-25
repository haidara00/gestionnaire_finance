from django.shortcuts import render
from .models import Debtor, Supplier, Debt, Credit
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, F, DecimalField
from decimal import Decimal
from django.db import models
from django.db.models import Value
from django.db.models.functions import Coalesce


from django.shortcuts import render, get_object_or_404, redirect
from .forms import DebtorForm, DebtForm, SupplierForm, CreditForm, PaymentForm, SupplierPaymentForm


# View for listing all Debtors
def debtor_list(request):
    query = request.GET.get('q')
    
    # Start with all debtors and ANNOTATE them with their remaining balance
    all_debtors = Debtor.objects.all().annotate(
        # Calculate the total of all debts for the debtor
        total_debt_amount=Coalesce(Sum('debts__amount'), Value(0, output_field=DecimalField())),
        # Calculate the total of all payments made to the debtor's debts
        total_paid_amount=Coalesce(Sum('debts__payments__amount'), Value(0, output_field=DecimalField())),
        # Calculate the remaining balance
        remaining_balance=F('total_debt_amount') - F('total_paid_amount')
    ).order_by('-created_at')
    
    # If a search query exists, filter the results
    if query:
        all_debtors = all_debtors.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(company__icontains=query) |
            models.Q(phone__icontains=query)
        )
    
    context = {'debtors': all_debtors, 'query': query}
    return render(request, 'core/debtor_list.html', context)
# View for listing all Suppliers
def supplier_list(request):
    query = request.GET.get('q')
    
    # Start with all suppliers and ANNOTATE them with their remaining balance
    all_suppliers = Supplier.objects.all().annotate(
        # Calculate the total of all credits for the supplier
        total_credit_amount=Coalesce(Sum('credits__amount'), Value(0, output_field=DecimalField())),
        # Calculate the total of all payments made to the supplier's credits
        total_paid_amount=Coalesce(Sum('credits__payments__amount'), Value(0, output_field=DecimalField())),
        # Calculate the remaining balance
        
        remaining_balance=F('total_credit_amount') - F('total_paid_amount')
    ).order_by('-created_at')
    
    
    if query:
        all_suppliers = all_suppliers.filter(
            models.Q(name__icontains=query) |
            models.Q(contact_person__icontains=query) |
            models.Q(phone__icontains=query)
        )
    
    
    context = {'suppliers': all_suppliers, 'query': query}
    return render(request, 'core/supplier_list.html', context)

# View for seeing the details of a single Debtor and their debts
def debtor_detail(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    debts = debtor.debts.all().order_by('-date_incurred')
    
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            new_payment = payment_form.save()
            return redirect('debtor-detail', debtor_id=debtor.id)
    else:
        payment_form = PaymentForm()
        
        # 1. Get the IDs of debts that have a remaining balance > 0
        debts_with_balance_ids = Debt.objects.filter(
            debtor=debtor
        ).annotate(
            total_paid=Coalesce(Sum('payments__amount'), Value(0, output_field=DecimalField()))
        ).annotate(
            remaining_balance=F('amount') - F('total_paid')
        ).filter(
            remaining_balance__gt=0
        ).values_list('id', flat=True)

        # 2. Filter the form's queryset using the list of IDs
        payment_form.fields['debt'].queryset = Debt.objects.filter(id__in=debts_with_balance_ids)
    
    context = {
        'debtor': debtor,
        'debts': debts,
        'payment_form': payment_form,
    }
    return render(request, 'core/debtor_detail.html', context)
# View for seeing the details of a single Supplier and their credits
def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    credits = supplier.credits.all().order_by('-date_incurred')
    
    if request.method == 'POST':
        payment_form = SupplierPaymentForm(request.POST)
        if payment_form.is_valid():
            new_payment = payment_form.save()
            return redirect('supplier-detail', supplier_id=supplier.id)
    else:
        # Create the form first
        payment_form = SupplierPaymentForm()
        
        # 1. Get the IDs of credits that have a remaining balance > 0
        # We use the annotation method just to calculate this list of IDs.
        credits_with_balance_ids = Credit.objects.filter(
            supplier=supplier
        ).annotate(
            total_paid=Coalesce(Sum('payments__amount'), Value(0, output_field=DecimalField()))
        ).annotate(
            remaining_balance=F('amount') - F('total_paid')
        ).filter(
            remaining_balance__gt=0
        ).values_list('id', flat=True) # This returns a flat list of IDs, e.g., [1, 3, 5]

        # 2. Now, filter the form's queryset to only include credits with those IDs
        payment_form.fields['credit'].queryset = Credit.objects.filter(id__in=credits_with_balance_ids)
    
    context = {
        'supplier': supplier,
        'credits': credits,
        'payment_form': payment_form,
    }
    return render(request, 'core/supplier_detail.html', context)
def debtor_create(request):
    if request.method == 'POST':
        # If the form has been submitted, process the data
        form = DebtorForm(request.POST)
        if form.is_valid():
            form.save() # This saves the new Debtor to the database
            return redirect('debtor-list') # Redirect to the list page after saving
    else:
        # If it's a normal GET request, show an empty form
        form = DebtorForm()
    
    context = {'form': form}
    return render(request, 'core/debtor_form.html', context)

# View for creating a new Debt
def debt_create(request):
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('debtor-list')
    else:
        form = DebtForm()
    
    context = {'form': form}
    return render(request, 'core/debt_form.html', context)

# Views for Supplier and Credit (they will look very similar)
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier-list')
    else:
        form = SupplierForm()
    
    context = {'form': form}
    return render(request, 'core/supplier_form.html', context)

def credit_create(request):
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier-list')
    else:
        form = CreditForm()
    
    context = {'form': form}
    return render(request, 'core/credit_form.html', context)


def dashboard(request):
    """
    Vue pour le tableau de bord principal.
    """
    # 1. Calculate Financial Totals
    total_debt = Debt.objects.aggregate(total=Sum('amount'))['total'] or Decimal(0)
    total_credit = Credit.objects.aggregate(total=Sum('amount'))['total'] or Decimal(0)
    net_balance = total_credit - total_debt

    # 2. Get Recent Activity
    recent_debtors = Debtor.objects.all().order_by('-created_at')[:5]
    recent_suppliers = Supplier.objects.all().order_by('-created_at')[:5]
    recent_debts = Debt.objects.select_related('debtor').order_by('-date_incurred')[:5]
    recent_credits = Credit.objects.select_related('supplier').order_by('-date_incurred')[:5]

    # 3. Prepare data for Charts - Top Debtors by REMAINING BALANCE
    top_debtors_by_balance = Debtor.objects.all()
    debtor_chart_data = []
    for debtor in top_debtors_by_balance:
        total_remaining = Decimal(0)
        for debt in debtor.debts.all():
            total_remaining += debt.remaining_balance
        if total_remaining > 0:  # Only include debtors with remaining balance
            debtor_chart_data.append({
                'name': f"{debtor.first_name} {debtor.last_name}",
                'balance': float(total_remaining)  # Chart.js needs floats
            })
    # Sort and get top 5
    debtor_chart_data.sort(key=lambda x: x['balance'], reverse=True)
    top_debtors_chart = debtor_chart_data[:5]

    # Extract labels and data for the chart
    debtor_labels = [item['name'] for item in top_debtors_chart]
    debtor_data = [item['balance'] for item in top_debtors_chart]

    # 4. Prepare data for Charts - Top Suppliers by REMAINING BALANCE
    top_suppliers_by_balance = Supplier.objects.all()
    supplier_chart_data = []
    for supplier in top_suppliers_by_balance:
        total_remaining = Decimal(0)
        for credit in supplier.credits.all():
            total_remaining += credit.remaining_balance
        if total_remaining > 0:  # Only include suppliers with remaining balance
            supplier_chart_data.append({
                'name': supplier.name,
                'balance': float(total_remaining)
            })
    # Sort and get top 5
    supplier_chart_data.sort(key=lambda x: x['balance'], reverse=True)
    top_suppliers_chart = supplier_chart_data[:5]

    # Extract labels and data for the chart
    supplier_labels = [item['name'] for item in top_suppliers_chart]
    supplier_data = [item['balance'] for item in top_suppliers_chart]

    context = {
        'total_debt': total_debt,
        'total_credit': total_credit,
        'net_balance': net_balance,
        'recent_debtors': recent_debtors,
        'recent_suppliers': recent_suppliers,
        'recent_debts': recent_debts,
        'recent_credits': recent_credits,
        'debtor_labels': debtor_labels,
        'debtor_data': debtor_data,
        'supplier_labels': supplier_labels,
        'supplier_data': supplier_data,
    }
    return render(request, 'core/dashboard.html', context)