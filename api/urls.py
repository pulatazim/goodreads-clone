from django.urls import path

from api.views import BookReviewDetailAPIView, BookReviewsAPIView
from rest_framework import routers
from api.views import BookReviewViewSet


app_name = 'api'

# router = routers.DefaultRouter()
# router.register('review', BookReviewViewSet, basename='review')
# urlpatterns = router.urls

urlpatterns = [
    path("reviews/", BookReviewsAPIView.as_view(), name="review-list"),

    path("reviews/<int:id>/", BookReviewDetailAPIView.as_view(), name="review-detail"),
]