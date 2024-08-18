# Import the BasePermission class from rest_framework.permissions
from rest_framework.permissions import BasePermission

# Custom permission class to check if the user is a Customer
class IsCustomer(BasePermission):
    # Method to check if the user has permission
    def has_permission(self, request, view):
        # Return True if the user is a customer, otherwise False
        return request.user.is_customer == True

# Custom permission class to check if the user is a Chef
class IsChef(BasePermission):
    # Method to check if the user has permission
    def has_permission(self, request, view):
        # Return True if the user is a chef, otherwise False
        return request.user.is_chef == True

# Custom permission class to check if the user is a Company
class IsCompany(BasePermission):
    # Method to check if the user has permission
    def has_permission(self, request, view):
        # Return True if the user is a company, otherwise False
        return request.user.is_company == True
