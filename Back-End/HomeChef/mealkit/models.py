from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model extending AbstractUser
class User(AbstractUser):
    is_chef = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

# Model representing a Company
class Company(models.Model):
    VEG = 'veg'
    NON_VEG = 'non_veg'
    BOTH = 'both'

    FOOD_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non-Vegetarian'),
        (BOTH, 'Both'),
    ]

    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'

    CATEGORY_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    email = models.EmailField()
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES, default=BOTH)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=LUNCH)

    def __str__(self):
        return self.company_name

# Model representing a Subscription Plan
class SubscriptionPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('2peopleperweek', '2 People Per Week Plan'),
        ('4peopleperweek', '4 People Per Week Plan'),
    ]

    plan_name = models.CharField(max_length=255, choices=PLAN_TYPE_CHOICES, default='2peopleperweek')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Duration of the subscription",null=True)
    meals_per_week = models.IntegerField()
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='subscription_plan')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_name

# Model representing a Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)
    age = models.IntegerField(null=True, blank=True)
    mobile = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    preferences = models.TextField(blank=True, null=True)
    dietary_restrictions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else "Unnamed Customer"

class Subscription(models.Model):
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Subscription for {self.customer_name} - {self.plan} ({self.start_date.date()} to {self.end_date.date()})"
    
# Model representing a Chef
class ChefProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chef_profile', null=True, blank=True)
    chef_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(blank=True, null=True)
    cooking_experience = models.IntegerField(help_text="Years of experience")
    speciality = models.CharField(max_length=255, help_text="Chef's speciality dishes")
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.chef_name if self.chef_name else "Unnamed Chef"

# Model representing a Meal Kit
class MealKit(models.Model):
    chef = models.ForeignKey(ChefProfile, on_delete=models.CASCADE, related_name='meal_kits')
    meal_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_time = models.DurationField(null=True)
    servings = models.IntegerField(null=True)
    ingredients = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.meal_name

class ChefKartService(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('one_time_cook', 'One-time Cook'),
        ('monthly_cook', 'Monthly Cook'),
        ('party_chef', 'Party Chef'),
    )

    chef = models.ForeignKey(ChefProfile, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Duration of the service")
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service_type} by {self.chef}"

class ChefServiceBooking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(ChefKartService, on_delete=models.CASCADE, related_name='bookings')
    event_type = models.CharField(max_length=255)
    booking_date = models.DateTimeField(auto_now_add=True)
    service_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking for {self.service} by {self.customer}"

class Order(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    PAYMENT_PENDING = 'Pending'
    PAID = 'Paid'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAID, 'Paid'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    meal_kit = models.ForeignKey(MealKit, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

# Model representing a Gift Card
class GiftCard(models.Model):
    GIFT_AMOUNT_CHOICES = [
        (70, '$70'),
        (100, '$100'),
        (150, '$150'),
    ]

    gift_type = models.CharField(max_length=255, default='Meal')
    gift_amount = models.IntegerField(choices=GIFT_AMOUNT_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    issue_date = models.DateTimeField(auto_now_add=True,null=True)
    expiry_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True,null=True)

    def __str__(self):
        return f"Gift Card {self.gift_type}"

# Model representing a CartItem
class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items',null=True)
    meal_kit = models.ForeignKey(MealKit, on_delete=models.CASCADE, related_name='cart_items',null=True)
    quantity = models.IntegerField(default=1,null=True)
    total_gift_amount=models.DecimalField(max_digits=10, decimal_places=2, null=True)
    gift_card = models.ForeignKey(GiftCard, on_delete=models.SET_NULL, null=True, blank=True, related_name='cart_items')

    def __str__(self):
        return f"CartItem {self.id} for {self.customer}"

# Model representing a Review
class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    meal_kit = models.ForeignKey(MealKit, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    review_date=models.DateTimeField()
    def __str__(self):
        return f"Review by {self.customer} for {self.meal_kit}"

# Model representing a Payment
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"

# Model representing a Delivery
class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    delivery_date = models.DateTimeField()
    delivery_address = models.TextField()
    delivery_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"Delivery {self.id} for Order {self.order.id}"
