from django.db import models
from django.core.validators import RegexValidator
"""from petzeno.models import User  # Import your custom User model
from petzeno.models import Pet """
"""User = get_user_model()"""

# Create your models here.
class Demo(models.Model):
    name=models.TextField(max_length=100)
    photo=models.ImageField(upload_to='pets_photos/')

    def _str_(self):
        return self.name

class User(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+91\d{10}$',
        message="Phone number must be entered in the format: '+91XXXXXXXXXX'. Up to 10 digits allowed after '+91'."
    )
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('guest','Guest'),
        ('admin','Admin'),
    ]
    id = models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=20)  
    email=models.EmailField()
    password=models.CharField(max_length=20)
    phone = models.CharField(validators=[phone_regex], max_length=13)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def _str_(self):
        return self.name

class Pet(models.Model):
    # Choices for species
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('fish','fish'),
        ('other', 'Other'),
    ]
    BREED_CHOICES = {
        'dog': [
            ('labrador', 'Labrador Retriever'),
            ('golden_retriever', 'Golden Retriever'),
            ('german_shepherd', 'German Shepherd'),
            ('bulldog', 'Bulldog'),
            ('poodle', 'Poodle'),
            ('other', 'Other'),
        ],
        'cat': [
            ('persian', 'Persian'),
            ('siamese', 'Siamese'),
            ('maine_coon', 'Maine Coon'),
            ('bengal', 'Bengal'),
            ('other', 'Other'),
        ],
    }
    # Choices for breed (example breeds, can be expanded)
    '''DOG_BREEDS = [
        ('labrador', 'Labrador Retriever'),
        ('golden_retriever', 'Golden Retriever'),
        ('german_shepherd', 'German Shepherd'),
        ('bulldog', 'Bulldog'),
        ('poodle', 'Poodle'),
        ('other', 'Other'),
    ]
    
    CAT_BREEDS = [
        ('persian', 'Persian'),
        ('siamese', 'Siamese'),
        ('maine_coon', 'Maine Coon'),
        ('bengal', 'Bengal'),
        ('other', 'Other'),
    ]'''

    # Choices for gender
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    # Choices for health status
    HEALTH_STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('vaccinated', 'Vaccinated'),
        ('neutered', 'Neutered'),
        ('special_needs', 'Special Needs'),
        ('other', 'Other'),
    ]

    # Choices for adoption status
    ADOPTION_STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('adopted', 'Adopted'),
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='pet_photos/')
    species = models.CharField(max_length=100, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=50, blank=True, null=True)  # Will be set dynamically
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    cost = models.IntegerField()
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES, blank=True)
    personality_traits = models.TextField(help_text="Describe the pet’s personality")
    adoption_status = models.CharField(max_length=20, choices=ADOPTION_STATUS_CHOICES, default='available')
    date_added = models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=255,help_text="enter city or address",default="Not specified")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="pets")#user can have multiple pets

    def __str__(self):
        return f"{self.name} ({self.get_species_display()}) - Added by {self.user.name}"

''' def get_breed_choices(self):
        """ Returns breed choices based on species """
        if self.species == 'dog':
            return self.DOG_BREEDS
        elif self.species == 'cat':
            return self.CAT_BREEDS
        return [('other', 'Other')]'''


class Wishlist(models.Model):
    user= models.ForeignKey('petzeno.User', on_delete=models.CASCADE)
    pet= models.ForeignKey('petzeno.Pet', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} added {self.pet} to wishlist"

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    pet = models.ForeignKey('petzeno.Pet', on_delete=models.CASCADE)
    buyer = models.ForeignKey('petzeno.User', on_delete=models.CASCADE, related_name='buyer_orders')
    seller = models.ForeignKey('petzeno.User', on_delete=models.CASCADE, related_name='seller_orders')
    request_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'),('rejected','Rejected')], default='pending')
    payment_status = models.BooleanField(default=False)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

from django.db import models

class Form(models.Model):
    id=models.ForeignKey('petzeno.Order',primary_key=True,unique=True,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    
    # Delivery Address
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)

    # Additional Notes
    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.full_name}"


class SuccessStory(models.Model):
    pet_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    story = models.TextField()
    image = models.ImageField(upload_to='pet_photos/', default='default_pet.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_name} & {self.owner_name}"
