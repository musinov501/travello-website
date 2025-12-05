from rest_framework import serializers
from apps.hotels.models.hotels import Hotel
from apps.tours.models.tours import Tour
from apps.excursions.models.excursion import Excursion
from apps.bookings.models.booking_model import Booking


class HotelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "location",
            "rating",
            "description",
            "price_per_night",
            "available_rooms",
            "is_available",
            "main_image"
        ]




class TourInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ["id", "title", "description", "price", "destination", "duration_days", "capacity","status", "image"]





class ExcursionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = ["id", "title", "location", "price", "description", "image", "duration_hours", "is_available"]


class BookingSerializer(serializers.ModelSerializer):
    hotel = HotelInfoSerializer(read_only=True)
    tour = TourInfoSerializer(read_only=True)
    excursion = ExcursionInfoSerializer(read_only=True)

    hotel_id = serializers.IntegerField(write_only=True, required=False)
    tour_id = serializers.IntegerField(write_only=True, required=False)
    excursion_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",

            # Full nested details (output)
            "hotel",
            "tour",
            "excursion",

            # Only IDs are writeable (input)
            "hotel_id",
            "tour_id",
            "excursion_id",

            "check_in",
            "check_out",
            "guests",
            "total_price",
            "status",
            "created_at"
        ]
        read_only_fields = ("user", "total_price", "status")

    def validate(self, data):
        hotel_id = data.get("hotel_id")
        tour_id = data.get("tour_id")
        excursion_id = data.get("excursion_id")

        selected = [hotel_id, tour_id, excursion_id]
        count = len([x for x in selected if x is not None])

        if count != 1:
            raise serializers.ValidationError(
                "You must choose exactly one of: hotel_id, tour_id, excursion_id."
            )

        # Hotel logic
        if hotel_id:
            if not data.get("check_in") or not data.get("check_out"):
                raise serializers.ValidationError("Hotel booking requires check-in & check-out.")

        else:
            if data.get("check_in") or data.get("check_out"):
                raise serializers.ValidationError(
                    "Check-in/check-out allowed only for hotels."
                )

        return data

    def create(self, validated_data):
        hotel_id = validated_data.pop("hotel_id", None)
        tour_id = validated_data.pop("tour_id", None)
        excursion_id = validated_data.pop("excursion_id", None)

        # Attach the selected item to validated_data
        if hotel_id:
            from apps.hotels.models import Hotel
            hotel = Hotel.objects.get(id=hotel_id)
            validated_data["hotel"] = hotel

        elif tour_id:
            from apps.tours.models import Tour
            validated_data["tour"] = Tour.objects.get(id=tour_id)

        elif excursion_id:
            from apps.excursions.models import Excursion
            validated_data["excursion"] = Excursion.objects.get(id=excursion_id)

        # User
        validated_data["user"] = self.context["request"].user

        # Price calculations
        hotel = validated_data.get("hotel")
        tour = validated_data.get("tour")
        excursion = validated_data.get("excursion")
        guests = validated_data.get("guests", 1)

        if hotel:
            nights = (validated_data["check_out"] - validated_data["check_in"]).days
            validated_data["total_price"] = hotel.price_per_night * nights * guests
            hotel.available_rooms -= guests
            hotel.save()

        elif tour:
            validated_data["total_price"] = tour.price * guests

        elif excursion:
            validated_data["total_price"] = excursion.price * guests

        return super().create(validated_data)
