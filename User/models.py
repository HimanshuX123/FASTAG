from django.db import models

from django.db.models import Sum


# Make sure Transaction is imported


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    ID_PROOF_CHOICES = [
        ('Aadhar', 'Aadhar'),
        ('PAN', 'PAN'),
        ('Driving License', 'Driving License'),
    ]

    VEHICLE_TYPE_CHOICES = [
        ('Car', 'Car'),
        ('Bike', 'Bike'),
        ('Truck', 'Truck'),
        ('Bus', 'Bus'),
        ('Other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)

    id_proof_type = models.CharField(max_length=20, choices=ID_PROOF_CHOICES)
    id_proof_number = models.CharField(max_length=20, unique=True)
    id_proof_upload = models.FileField(upload_to='id_proofs/')

    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    vehicle_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=15, unique=True)
    rc_copy = models.FileField(upload_to='rc_copies/')

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    def update_balance(self):
        """ Updates the user’s balance based on all completed payments. """
        total_balance = Payment.objects.filter(user=self).aggregate(Sum('amount'))
        self.balance = total_balance['amount__sum'] or 0
        self.save()

    @property
    def balance(self):
        total_balance = Payment.objects.filter(user=self).aggregate(Sum('amount'))
        return total_balance['amount__sum'] or 0  # Return 0 if no transactions

    # Return 0 if no transactions
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.vehicle_number}"


class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
            """Automatically add the payment amount to the user's balance upon saving."""
            super().save(*args, **kwargs)  # Save the payment record
            # Update user balance immediately
            self.user.refresh_from_db()

    def __str__(self):
            return f"{self.user.first_name} {self.user.last_name} - ₹{self.amount}"


