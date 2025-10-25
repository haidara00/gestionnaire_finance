from django import forms
from .models import Debtor, Debt, Supplier, Credit, Payment, SupplierPayment

# Form for adding a new Debtor
class DebtorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's 'form-control' class to every field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Make specific fields use a textarea for better input
            if field_name == 'address':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})

    
    class Meta:
        model = Debtor
        fields = ['first_name', 'last_name', 'company', 'email', 'phone', 'address']
# Form for adding a new Debt
class DebtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's 'form-control' class to every field
        for field_name, field in self.fields.items():

            field.widget.attrs['class'] = 'form-control'
            # Make specific fields use a textarea for better input
            if field_name == 'description':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            if field_name == 'date_incurred':
                field.widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
            if field_name == 'amount':
                field.widget = forms.NumberInput(attrs={'class': 'form-control', 'step': '10000.00'})
            if field_name == 'debtor':    
                pass
   

            
            
    class Meta:
        model = Debt
        fields = ['debtor', 'amount', 'description', 'date_incurred']
        

# Form for adding a new Supplier
class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's 'form-control' class to every field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Make specific fields use a textarea for better input
            if field_name == 'address':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            if field_name == 'contact_person':
                field.widget = forms.TextInput(attrs={'class': 'form-control'})
            if field_name == 'email':
                field.widget = forms.EmailInput(attrs={'class': 'form-control'})
            if field_name == 'phone':
                field.widget = forms.TextInput(attrs={'class': 'form-control'})
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address']

# Form for adding a new Credit
class CreditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's 'form-control' class to every field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Make specific fields use a textarea for better input
            if field_name == 'address':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            if field_name == 'description':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            if field_name == 'date_incurred':
                field.widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
            if field_name == 'amount':
                field.widget = forms.NumberInput(attrs={'class': 'form-control', 'step': '10000.00'})
            if field_name == 'supplier':    
                pass
            
    class Meta:
        model = Credit
        fields = ['supplier', 'amount', 'description', 'date_incurred']
        widgets = {
            'date_incurred': forms.DateInput(attrs={'type': 'date'})
        }
        
class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's 'form-control' class to every field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Make specific fields use a textarea for better input
            if field_name == 'address':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            if field_name == 'notes':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            if field_name == 'date_paid':
                field.widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
            if field_name == 'amount':
                field.widget = forms.NumberInput(attrs={'class': 'form-control', 'step': '10000.00'})
            if field_name == 'debt':
                pass    

    class Meta:
        model = Payment
        fields = ['debt', 'amount', 'date_paid', 'notes']
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'})
        }
        
class SupplierPaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap's 'form-control' class to every field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Make specific fields use a textarea for better input
            if field_name == 'address':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            if field_name == 'notes':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            if field_name == 'date_paid':
                field.widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
            if field_name == 'amount':
                field.widget = forms.NumberInput(attrs={'class': 'form-control', 'step': '10000.00'})
            if field_name == 'credit':    
                pass
    class Meta:
        model = SupplierPayment
        fields = ['credit', 'amount', 'date_paid', 'notes']
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'})
        }
