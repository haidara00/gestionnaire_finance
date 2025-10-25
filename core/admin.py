from django.contrib import admin
from .models import Debtor, Debt, Supplier, Credit
from .models import Payment, SupplierPayment # <-- Import the new model

# Register your models here.

# Customize how the Debtor model looks in the admin
class DebtorAdmin(admin.ModelAdmin):
    # This defines which columns are displayed in the list view
    list_display = ('first_name', 'last_name', 'company', 'phone', 'total_debt_display', 'created_at')
    # This adds a search box. You can search by these fields.
    search_fields = ('first_name', 'last_name', 'company', 'phone')
    # This adds filters on the right side of the list view
    list_filter = ('created_at',)
    
    # This is a custom method to display the total_debt property in the admin list
    def total_debt_display(self, obj):
        return f"{obj.total_debt:,.2f} FCFA"  # Formats the number with commas and 2 decimal places
    total_debt_display.short_description = 'Total Dette'  # Sets the column header

# Register the Debtor model with its custom admin class
admin.site.register(Debtor, DebtorAdmin)

# A simpler registration for Debt. We can customize it later if needed.
class DebtAdmin(admin.ModelAdmin):
    list_display = ('debtor', 'amount', 'description', 'date_incurred')
    list_filter = ('date_incurred',)
    search_fields = ('debtor__first_name', 'debtor__last_name', 'description') # Note: searching across relationships with __

admin.site.register(Debt, DebtAdmin)

# Customize the Supplier admin
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'total_credit_display', 'created_at')
    search_fields = ('name', 'contact_person', 'phone')
    list_filter = ('created_at',)
    
    def total_credit_display(self, obj):
        return f"{obj.total_credit:,.2f} FCFA"
    total_credit_display.short_description = 'Total Crédit'

admin.site.register(Supplier, SupplierAdmin)

# Register the Credit model
class CreditAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'amount', 'description', 'date_incurred')
    list_filter = ('date_incurred',)
    search_fields = ('supplier__name', 'description')

admin.site.register(Credit, CreditAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('debt', 'amount', 'date_paid', 'debtor_name')
    list_filter = ('date_paid',)
    search_fields = ('debt__debtor__first_name', 'debt__debtor__last_name', 'notes')

    # A custom method to display the debtor's name in the admin list
    def debtor_name(self, obj):
        return obj.debt.debtor
    debtor_name.short_description = 'Débiteur'
admin.site.register(Payment, PaymentAdmin)

class SupplierPaymentAdmin(admin.ModelAdmin):
    list_display = ('credit', 'amount', 'date_paid', 'supplier_name')
    list_filter = ('date_paid',)
    search_fields = ('credit__supplier__name', 'notes')

    # A custom method to display the supplier's name
    def supplier_name(self, obj):
        return obj.credit.supplier
    supplier_name.short_description = 'Fournisseur'

admin.site.register(SupplierPayment, SupplierPaymentAdmin)