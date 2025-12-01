from django.db import models
from django.utils import timezone


class DeviceManager(models.Manager):


    # Filter methods
    def active(self):

        return self.filter(is_active=True)

    def for_user(self, user):

        return self.filter(user=user)

    def by_device_type(self, device_type):

        return self.filter(device_type=device_type)

    def with_push_enabled(self):

        return self.filter(is_push_notification=True)

    # Business logic methods
    def get_active_devices(self, user):

        return self.filter(user=user, is_active=True).order_by('-last_login')

    def logout_all_devices(self, user):

        return self.filter(user=user, is_active=True).update(
            is_active=False,
            logged_out_at=timezone.now()
        )

    def logout_other_devices(self, user, current_device_id):

        return self.filter(
            user=user,
            is_active=True
        ).exclude(
            id=current_device_id
        ).update(
            is_active=False,
            logged_out_at=timezone.now()
        )

    def is_token_valid(self, refresh_token_jti):

        return self.filter(
            refresh_token_jti=refresh_token_jti,
            is_active=True
        ).exists()

    def get_by_token(self, refresh_token_jti):
        
        return self.get(refresh_token_jti=refresh_token_jti)

    def create_device_session(self, user, device_data, refresh_token_jti):
        
        return self.create(
            user=user,
            refresh_token_jti=refresh_token_jti,
            is_active=True,
            **device_data
        )
