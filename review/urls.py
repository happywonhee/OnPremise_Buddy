from django.urls import path
from . import views

app_name='review'
urlpatterns = [
    path('', views.ReviewList.as_view(), name='list'),
    path('<int:pk>/', views.ReviewDetail.as_view(), name='detail'),
    path('create_review/', views.ReviewCreate.as_view(),name='review_create'),
    path('delete_review/<int:pk>/', views.ReviewDelete,name='review_delete'),
    path('update_review/<int:pk>/', views.ReviewUpdate.as_view(),name='review_update'),
]
