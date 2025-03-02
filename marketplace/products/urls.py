from django.urls import path
from .views import (
    CategoryListCreateView, CategoryRetrieveUpdateDeleteView,
    ProductListCreateView, ProductRetrieveUpdateDeleteView
)

urlpatterns = [
    # Category Endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDeleteView.as_view(), name='category-detail'),

    # Product Endpoints
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-detail'),
]
