from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError

from apps.testimonials.models.testimonials import Testimonial
from apps.testimonials.serializers.testimonial_serializer import TestimonialSerializer
from apps.shared.utils.custom_response import CustomResponse


class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.filter(is_published=True)
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        testimonials = self.get_queryset()
        serializer = self.get_serializer(testimonials, many=True)

        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data,
            count=testimonials.count()
        )


class TestimonialDetailView(generics.RetrieveAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        try:
            testimonial = self.get_object()
        except Exception:
            return CustomResponse.not_found(
                message_key="NOT_FOUND",
                request=request
            )

        serializer = self.get_serializer(testimonial)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class TestimonialCreateView(generics.CreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )

        testimonial = serializer.save()

        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=TestimonialSerializer(testimonial).data
        )


class TestimonialUpdateView(generics.UpdateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )

        testimonial = serializer.save()

        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=TestimonialSerializer(testimonial).data
        )


class TestimonialDeleteView(generics.DestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        testimonial = self.get_object()
        testimonial_id = testimonial.id
        testimonial.delete()

        return CustomResponse.success(
            message_key="DELETED",
            request=request,
            data={"id": testimonial_id}
        )


