from django.contrib import admin
from .models import *

# Customize the User model admin interface
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_chef', 'is_customer', 'is_company', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_chef', 'is_customer', 'is_company', 'is_staff', 'is_active')

# Customize the Company model admin interface
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'food_type', 'category')
    search_fields = ('company_name', 'email')
    list_filter = ('food_type', 'category')

# Customize the SubscriptionPlan model admin interface
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'description', 'price', 'meals_per_week', 'company', 'is_active')
    search_fields = ('plan_name', 'company__company_name')
    list_filter = ('price', 'is_active')

# Customize the Customer model admin interface
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'gender', 'age', 'mobile', 'address', 'preferences', 'dietary_restrictions')
    search_fields = ('customer_name', 'user__username', 'mobile')
    list_filter = ('gender',)

# Customize the Subscription model admin interface
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'plan', 'start_date', 'end_date', 'is_active')
    search_fields = ('customer_name__user__username', 'plan__plan_name')
    list_filter = ('plan__plan_name', 'is_active', 'start_date', 'end_date')

# Customize the ChefProfile model admin interface
class ChefProfileAdmin(admin.ModelAdmin):
    list_display = ('chef_name', 'cooking_experience', 'speciality', 'rating')
    search_fields = ('chef_name', 'user__username')
    list_filter = ('cooking_experience', 'rating')

# Customize the MealKit model admin interface
class MealKitAdmin(admin.ModelAdmin):
    list_display = ('meal_name', 'price', 'chef', 'is_available')
    search_fields = ('meal_name', 'chef__user__username')
    list_filter = ('price', 'is_available')

# Customize the ChefKartService model admin interface
class ChefKartServiceAdmin(admin.ModelAdmin):
    list_display = ('chef', 'service_type', 'price', 'duration', 'available')
    search_fields = ('chef__user__username', 'service_type')
    list_filter = ('service_type', 'price', 'available')

# Customize the ChefServiceBooking model admin interface
class ChefServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'event_type', 'booking_date', 'service_date', 'status', 'total_price')
    search_fields = ('customer__user__username', 'service__service_type')
    list_filter = ('status', 'booking_date', 'service_date')

# Customize the Order model admin interface
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'meal_kit', 'quantity', 'total_amount', 'status', 'payment_status', 'order_date')
    search_fields = ('customer__user__username', 'meal_kit__meal_name')
    list_filter = ('status', 'payment_status', 'order_date')

# Customize the GiftCard model admin interface
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ('gift_type', 'gift_amount','expiry_date','quantity',)
    search_fields = ('gift_type', 'customer__user__username')
    list_filter = ('gift_amount',)

# Customize the CartItem model admin interface
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'gift_card', 'quantity')
    search_fields = ('customer__user__username', 'gift_card__gift_type')
    list_filter = ('quantity',)

# Customize the Review model admin interface
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'meal_kit', 'rating', 'comment', 'review_date')
    search_fields = ('customer__user__username', 'meal_kit__meal_name')
    list_filter = ('rating', 'review_date')

# Customize the Payment model admin interface
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'payment_date')
    search_fields = ('order__id', 'payment_method')
    list_filter = ('payment_method', 'payment_date')

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_date', 'delivery_address', 'delivery_status')
    search_fields = ('order__id', 'delivery_date')
    list_filter = ('delivery_date', 'delivery_status')



# Register models and their corresponding admin classes with the Django admin site
admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ChefProfile, ChefProfileAdmin)
admin.site.register(MealKit, MealKitAdmin)
admin.site.register(ChefKartService, ChefKartServiceAdmin)
admin.site.register(ChefServiceBooking, ChefServiceBookingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(GiftCard, GiftCardAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Delivery,DeliveryAdmin)
