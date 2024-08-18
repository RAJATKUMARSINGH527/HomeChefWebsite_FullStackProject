from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

# Serializer for the Company model
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

# Serializer for registering a new Company
class CompanyRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'password', 'email', 'food_type', 'category']

    def create(self, validated_data):
        company_name = validated_data.get('company_name')
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        email = validated_data.get('email')
        user = User.objects.create_user(username=company_name, password=hashed_password, email=email, is_company=True)
        company = Company.objects.create(user=user, **validated_data)
        return company

# Serializer for the SubscriptionPlan model
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

# Serializer for the Customer model
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# Serializer for registering a new Customer
class CustomerRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'customer_name', 'age', 'gender', 'mobile', 'address']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = User.objects.create_user(username=username, password=password, email=email, is_customer=True)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
    
# Serializer for the Subscription model
class SubscriptionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'

# Serializer for the ChefProfile model
class ChefProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefProfile
        fields = '__all__'

# Serializer for registering a new ChefProfile
class ChefProfileRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ChefProfile
        fields = ['id', 'chef_name', 'password', 'cooking_experience', 'speciality', 'rating']

    def create(self, validated_data):
        chef_name = validated_data.get('chef_name')
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        user = User.objects.create_user(username=chef_name, password=hashed_password, is_chef=True)
        chef = ChefProfile.objects.create(user=user, **validated_data)
        return chef

# Serializer for the MealKit model
class MealKitSerializer(serializers.ModelSerializer):
    chef = ChefProfileSerializer(read_only=True)

    class Meta:
        model = MealKit
        fields = '__all__'

# Serializer for the ChefKartService model
class ChefKartServiceSerializer(serializers.ModelSerializer):
    chef = ChefProfileSerializer(read_only=True)

    class Meta:
        model = ChefKartService
        fields = '__all__'

# Serializer for the ChefServiceBooking model
class ChefServiceBookingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    service = ChefKartServiceSerializer(read_only=True)

    class Meta:
        model = ChefServiceBooking
        fields = '__all__'

# Serializer for the Order model
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    meal_kit = MealKitSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

# Serializer for the GiftCard model
class GiftCardSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = GiftCard
        fields = '__all__'

# Serializer for the CartItem model
class CartItemSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    gift_card = GiftCardSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'

# Serializer for the Review model
class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    meal_kit = MealKitSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

# Serializer for the Payment model
class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

# Serializer for the Delivery model
class DeliverySerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    
    class Meta:
        model = Delivery
        fields = '__all__'
