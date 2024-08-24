# Import necessary modules and classes from rest_framework and other packages
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken ,BlacklistedToken
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsChef,IsCompany,IsCustomer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi


# Custom Pagination Class
class CustomPagination(PageNumberPagination):
    # Set default page size
    page_size = 2
    # Allow clients to override the page size using the `page_size` query parameter
    page_size_query_param = 'page_size'
    # Set the maximum page size
    max_page_size = 10

# Customer Register View
class CustomerRegisterView(generics.CreateAPIView):
    # Allow any user to access this view
    permission_classes = [AllowAny]
    # Use the CustomerRegisterSerializer for this view
    serializer_class = CustomerRegisterSerializer

    def post(self, request, *args, **kwargs):
        # Serialize the incoming data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the new customer if the data is valid
            customer = serializer.save()
            # Return a success response with the new customer's ID
            return Response({'detail': 'Customer registered successfully', 'customer_id': customer.id}, status=status.HTTP_201_CREATED)
        # Return validation errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View (JWT Authentication)
class UserLoginView(APIView):
    # Allow any user to access this view
    permission_classes = [AllowAny]
   
    @swagger_auto_schema( request_body=LoginSerializer, responses={200: 'Success', 400: 'Invalid Credentials'} )

    def post(self, request, *args, **kwargs):
        serializer=LoginSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        # Get username and password from the request data
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        # Find the user by username
        user = User.objects.filter(username=username).first()

        if user is not None:
            # Check the type of user and generate JWT tokens
            if user.is_customer or user.is_company or user.is_chef:
                refresh = RefreshToken.for_user(user)
                if user.is_customer:
                    user_type = 'customer'
                elif user.is_company:
                    user_type = 'company'
                else:
                    user_type = 'chef'
                # Return the JWT tokens and user type
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_type': user_type
                })
            else:
                # Return an error if the user type is not recognized
                return Response({'detail': 'User type not recognized'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Return an error if the credentials are invalid
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
    def post(self,request):
        try:
            token=OutstandingToken.objects.filter(user=request.user).latest('created_at')
            BlacklistedToken.objects.create(token=token)
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

# Customer List View
class CustomerListView(generics.ListAPIView):
    # Define the queryset to retrieve all Customer objects
    queryset = Customer.objects.all()
    # Use CustomerSerializer to serialize the queryset
    serializer_class = CustomerSerializer
    permission_classes = [IsCompany]  # Only companies can view customers
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['customer_name', 'age']
    # Define ordering fields
    ordering_fields = ['customer_name', 'age']
    # Define filterset fields
    filterset_fields = ['customer_name']

# Customer Detail View
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Customer objects
    queryset = Customer.objects.all()
    # Use CustomerSerializer to serialize the queryset
    serializer_class = CustomerSerializer

    permission_classes = [IsCustomer]  # Only the customer themselves can update/delete their profile
    def get_object(self):
        user=super().get_object(self)
        if self.request.user.username!=user.username:
            PermissionDenied(detail='You do not have permission to access this user')
        return user

# Company Register  Views
class CompanyRegisterView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanyRegisterSerializer

# Company List Views
class CompanyListView(generics.ListAPIView):
    # permission_classes=[IsCustomer]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = CustomPagination  
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['food_type', 'category']
    # Define ordering fields
    ordering_fields = ['company_name', 'food_type']
    # Define filterset fields
    filterset_fields = ['company_name']


   
class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # Only authenticated companies can view and create other companies
    permission_classes=[IsCompany]
    def get_object(self):
        company=super().get_object(self)
        if self.request.user.username!=company.company_name:
            PermissionDenied(detail='You do not have permission to access this user')
        return company

# Chef Register  Views
class ChefProfileRegisterView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset = ChefProfile.objects.all()
    serializer_class = ChefProfileRegisterSerializer

# ChefProfile List View
class ChefProfileListView(generics.ListAPIView):
    # Define the queryset to retrieve all ChefProfile objects
    queryset = ChefProfile.objects.all()
    # Use ChefProfileSerializer to serialize the queryset
    serializer_class = ChefProfileSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    permission_classes = [IsCompany,IsCustomer]  # Only authenticated companies can view and create chef profiles
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['chef_name', 'cooking_experience', 'speciality']
    # Define ordering fields
    ordering_fields = ['chef_name', 'rating']
    # Define filterset fields
    filterset_fields = ['speciality']




# ChefProfile Detail View
class ChefProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all ChefProfile objects
    queryset = ChefProfile.objects.all()
    # Use ChefProfileSerializer to serialize the queryset
    serializer_class = ChefProfileSerializer
    permission_classes = [IsChef]  # Only the chef themselves can update/delete their profile
    def get_object(self):
        chef=super().get_object(self)
        if self.request.user.username!=chef.chef_name:
            PermissionDenied(detail='You do not have permission to access this user')
        return chef
    
# Subscription Plan List View
class SubscriptionPlanListView(generics.ListAPIView):
    # Define the queryset to retrieve all SubscriptionPlan objects
    queryset = SubscriptionPlan.objects.all()
    # Use SubscriptionPlanSerializer to serialize the queryset
    serializer_class = SubscriptionPlanSerializer
    permission_classes=[AllowAny]
     # Use the custom pagination class
    pagination_class = CustomPagination
   
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['price', 'meals_per_week', 'company__company_name']
    # Define ordering fields
    ordering_fields = ['price', 'meals_per_week']
    # Define filterset fields
    filterset_fields = ['price']

# Subscription Plan List View
class SubscriptionPlanCreateView(generics.CreateAPIView):
    # Define the queryset to retrieve all SubscriptionPlan objects
    queryset = SubscriptionPlan.objects.all()
    # Use SubscriptionPlanSerializer to serialize the queryset
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsCompany]  # Only authenticated companies can view and create subscription plans
   

# Subscription Plan Detail View
class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all SubscriptionPlan objects
    queryset = SubscriptionPlan.objects.all()
    # Use SubscriptionPlanSerializer to serialize the queryset
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsCustomer]  # Only the company can update/delete their subscription plans

# Subscription List View
class SubscriptionListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all Subscription objects
    queryset = Subscription.objects.all()
    # Use SubscriptionSerializer to serialize the queryset
    serializer_class = SubscriptionSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    permission_classes = [IsCustomer]  # Only authenticated customers can view and create subscriptions
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['customer__customer_name', 'plan__plan_name']
    # Define ordering fields
    ordering_fields = ['start_date', 'end_date']
    # Define filterset fields
    filterset_fields = ['start_date', 'end_date']

# Subscription Detail View
class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Subscription objects
    queryset = Subscription.objects.all()
    # Use SubscriptionSerializer to serialize the queryset
    serializer_class = SubscriptionSerializer
    permission_classes = [IsCustomer]  # Only the customer themselves can update/delete their subscriptions


# Meal Kit List View
class MealKitListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all MealKit objects
    queryset = MealKit.objects.all()
    # Use MealKitSerializer to serialize the queryset
    serializer_class = MealKitSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Only authenticated companies can view and create meal kits
    permission_classes = [IsCompany]
    permission_classes = [IsChef]  
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['meal_name', 'ingredients', 'company__company_name']
    # Define ordering fields
    ordering_fields = ['meal_name', 'price']
    # Define filterset fields
    filterset_fields = ['meal_name']

# Meal Kit Detail View
class MealKitDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all MealKit objects
    queryset = MealKit.objects.all()
    # Use MealKitSerializer to serialize the queryset
    serializer_class = MealKitSerializer
    permission_classes = [IsCompany]  # Only the company can update/delete their meal kits


# Gift Card List View
class GiftCardListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all GiftCard objects
    queryset = GiftCard.objects.all()
    # Use GiftCardSerializer to serialize the queryset
    serializer_class = GiftCardSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    permission_classes = [IsCustomer]  # Only authenticated customers can view and create gift cards
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['card_number', 'amount', 'customer__customer_name']
    # Define ordering fields
    ordering_fields = ['amount', 'expiry_date']
    # Define filterset fields
    filterset_fields = ['expiry_date']

# Gift Card Detail View
class GiftCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all GiftCard objects
    queryset = GiftCard.objects.all()
    # Use GiftCardSerializer to serialize the queryset
    serializer_class = GiftCardSerializer
    permission_classes = [IsCustomer]  # Only the customer themselves can update/delete their gift cards

# Cart Item List View
class CartItemListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all CartItem objects
    queryset = CartItem.objects.all()
    # Use CartItemSerializer to serialize the queryset
    serializer_class = CartItemSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    permission_classes = [IsCustomer]  # Only authenticated customers can view and create cart items
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['quantity', 'meal_kit__meal_name']
    # Define ordering fields
    ordering_fields = ['quantity', 'meal_kit']
    # Define filterset fields
    filterset_fields = ['quantity']

# Cart Item Detail View
class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all CartItem objects
    queryset = CartItem.objects.all()
    # Use CartItemSerializer to serialize the queryset
    serializer_class = CartItemSerializer
    permission_classes = [IsCustomer]  # Only the customer themselves can update/delete their cart items
# Order List View
class OrderListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all Order objects
    queryset = Order.objects.all()
    # Use OrderSerializer to serialize the queryset
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]  # Only authenticated customers can view and create orders
    # Use the custom pagination class
    pagination_class = CustomPagination
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['customer__customer_name', 'total_amount']
    # Define ordering fields
    ordering_fields = ['total_amount', 'status']
    # Define filterset fields
    filterset_fields = ['status']

# Order Detail View
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Order objects
    queryset = Order.objects.all()
    # Use OrderSerializer to serialize the queryset
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]  # Only the customer themselves can update/delete their orders


# Review List View
class ReviewListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all Review objects
    queryset = Review.objects.all()
    # Use ReviewSerializer to serialize the queryset
    serializer_class = ReviewSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    permission_classes = [IsCustomer]  # Only authenticated customers can view and create reviews
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['review_text', 'rating', 'meal_kit__meal_name']
    # Define ordering fields
    ordering_fields = ['rating', 'review_date']
    # Define filterset fields
    filterset_fields = ['rating']

# Review Detail View
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Review objects
    queryset = Review.objects.all()
    # Use ReviewSerializer to serialize the queryset
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomer]  # Only the customer themselves can update/delete their reviews

# Delivery List View
class DeliveryListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all Delivery objects
    queryset = Delivery.objects.all()
    # Use DeliverySerializer to serialize the queryset
    serializer_class = DeliverySerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    permission_classes = [IsCompany]  # Only authenticated companies can view and create deliveries
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['delivery_date', 'delivery_status']
    # Define ordering fields
    ordering_fields = ['delivery_date', 'delivery_status']
    # Define filterset fields
    filterset_fields = ['delivery_status']

# Delivery Detail View
class DeliveryDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Delivery objects
    queryset = Delivery.objects.all()
    # Use DeliverySerializer to serialize the queryset
    serializer_class = DeliverySerializer
    permission_classes = [IsCompany]  # Only the company can update/delete their deliveries

# Payment List View
class PaymentListView(generics.ListCreateAPIView):
    # Define the queryset to retrieve all Payment objects
    queryset = Payment.objects.all()
    # Use PaymentSerializer to serialize the queryset
    serializer_class = PaymentSerializer
    # Use the custom pagination class
    pagination_class = CustomPagination
    permission_classes = [IsCustomer]  # Only authenticated customer can view and create payments
    # Add filter backends for searching, ordering, and filtering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # Define search fields
    search_fields = ['payment_date', 'amount', 'customer__customer_name']
    # Define ordering fields
    ordering_fields = ['payment_date', 'amount']
    # Define filterset fields
    filterset_fields = ['payment_date']

# Payment Detail View
class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to retrieve all Payment objects
    queryset = Payment.objects.all()
    # Use PaymentSerializer to serialize the queryset
    serializer_class = PaymentSerializer
    permission_classes = [IsCompany,IsCustomer]  # Only the company can update/delete their payments
