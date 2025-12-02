from rest_framework import generics, permissions
from apps.testimonials.models.testimonials import Testimonial
from apps.testimonials.serializers.testimonial_serializer import TestimonialSerializer


class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.filter(is_published=True)
    serializer_class = TestimonialSerializer

class TestimonialDetailView(generics.RetrieveAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class TestimonialCreateView(generics.CreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAdminUser]

class TestimonialUpdateView(generics.UpdateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAdminUser]

class TestimonialDeleteView(generics.DestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAdminUser]
