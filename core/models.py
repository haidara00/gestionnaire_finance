from django.db import models

# Model for Debtor (Débiteur)
class Debtor(models.Model):
    # Basic Information
    first_name = models.CharField(max_length=100, verbose_name="prénom")
    last_name = models.CharField(max_length=100, verbose_name="nom")
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name="entreprise")
    
    # Contact Information
    email = models.EmailField(blank=True, null=True, verbose_name="adresse e-mail")
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name="numéro de téléphone")
    address = models.TextField(blank=True, null=True, verbose_name="adresse")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="date de modification")

    # Metadata for Django
    class Meta:
        verbose_name = "Débiteur"
        verbose_name_plural = "Débiteurs"
        ordering = ['-created_at'] # Newest debtors first

    # This defines how the model is displayed as a string
    def __str__(self):
        if self.company:
            return f"{self.company} ({self.first_name} {self.last_name})"
        return f"{self.first_name} {self.last_name}"
    
    def get_remaining_balance(self):
        total_debt = sum(debt.amount for debt in self.debts.all())
        total_paid = sum(payment.amount for debt in self.debts.all() for payment in debt.payments.all())
        return total_debt - total_paid

    # This property will calculate the total debt for this debtor
    @property
    def total_debt(self):
        # We will create the Debt model next. This will sum all related Debt amounts.
        total = self.debts.aggregate(total=models.Sum('amount'))['total']
        return total if total is not None else 0.0


# Model for Debt (Dette)
class Debt(models.Model):
    # Link to the Debtor. 'on_delete=models.CASCADE' means if a debtor is deleted, all their debts are deleted too.
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, related_name='debts', verbose_name="débiteur")
    
    # Debt Information
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="montant")
    description = models.TextField(verbose_name="description")
    date_incurred = models.DateField(verbose_name="date de la dette")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dette"
        verbose_name_plural = "Dettes"
        ordering = ['-date_incurred'] # Most recent debts first

    def __str__(self):
        return f"Dette de {self.amount} FCFA - {self.debtor}"
    
    # ADD THIS PROPERTY

    @property
    def remaining_balance(self):
        """Calculates the remaining balance to be paid on this debt."""
        from decimal import Decimal # Import Decimal at the top of the file or here
        total_paid = self.payments.aggregate(total=models.Sum('amount'))['total']
        # Convert None to Decimal(0), not float(0.0)
        total_paid = total_paid if total_paid is not None else Decimal(0)
        return self.amount - total_paid # Decimal - Decimal = Correct!

    # You can also add a property for the status
    @property
    def status(self):
        balance = self.remaining_balance
        if balance <= 0:
            return "Soldé"
        else:
            return "En Cours"


# Model for Supplier (Fournisseur)
class Supplier(models.Model):
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="nom du fournisseur")
    contact_person = models.CharField(max_length=200, blank=True, null=True, verbose_name="personne à contacter")
    
    # Contact Information (same as Debtor)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def get_remaining_balance(self):
        total_credit = sum(credit.amount for credit in self.credits.all())
        total_paid = sum(payment.amount for credit in self.credits.all() for payment in credit.payments.all())
        return total_credit - total_paid

    # Property to calculate total credit for this supplier
    @property
    def total_credit(self):
        total = self.credits.aggregate(total=models.Sum('amount'))['total']
        return total if total is not None else 0.0


# Model for Credit (Crédit)
class Credit(models.Model):
    # Link to the Supplier
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='credits', verbose_name="fournisseur")
    
    # Credit Information
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="montant")
    description = models.TextField(verbose_name="description")
    date_incurred = models.DateField(verbose_name="date du crédit")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Crédit"
        verbose_name_plural = "Crédits"
        ordering = ['-date_incurred']

    def __str__(self):
        return f"Crédit de {self.amount} FCFA - {self.supplier}"
    
    # You can also add a property for the status
    @property
    def remaining_balance(self):
        """Calculates the remaining balance to be paid to the supplier."""
        from decimal import Decimal
        total_paid = self.payments.aggregate(total=models.Sum('amount'))['total']
        total_paid = total_paid if total_paid is not None else Decimal(0)
        return self.amount - total_paid
    
    @property
    def status(self):
        balance = self.remaining_balance
        if balance <= 0:
            return "Soldé"
        else:
            return "En Cours"
    
# Add this to your existing models in core/models.py

class Payment(models.Model):
    # Link to the Debt. If a Debt is deleted, all its payments are also deleted.
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE, related_name='payments', verbose_name="dette")
    
    # Payment Information
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="montant payé")
    date_paid = models.DateField(verbose_name="date de paiement")
    notes = models.TextField(blank=True, null=True, verbose_name="notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date_paid'] # Most recent payments first

    def __str__(self):
        return f"Paiement de {self.amount} FCFA le {self.date_paid}"

class SupplierPayment(models.Model):
    # Link to the Credit (what you owe the supplier)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='payments', verbose_name="crédit")
    
    # Payment Information
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="montant payé")
    date_paid = models.DateField(verbose_name="date de paiement")
    notes = models.TextField(blank=True, null=True, verbose_name="notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paiement Fournisseur"
        verbose_name_plural = "Paiements Fournisseurs"
        ordering = ['-date_paid']

    def __str__(self):
        return f"Paiement de {self.amount} FCFA le {self.date_paid}"

    