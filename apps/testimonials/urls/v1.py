from django.urls import path
from apps.testimonials.views.testimonial_view import (
    TestimonialCreateView,
    TestimonialListView,
    TestimonialDetailView,
    TestimonialDeleteView,
    TestimonialUpdateView
)


app_name = 'testimonials'

urlpatterns = [
    path('', TestimonialListView.as_view(), name='testimonial-list'),
    path('create/', TestimonialCreateView.as_view(), name='testimonial-create'),
    path('<int:pk>/', TestimonialDetailView.as_view(), name='testimonial-detail'),
    path('<int:pk>/update/', TestimonialUpdateView.as_view(), name='testimonial-update'),
    path('<int:pk>/delete/', TestimonialDeleteView.as_view(), name='testimonial-delete')
]


