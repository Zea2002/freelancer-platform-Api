from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return smart_str(user.pk) + smart_str(timestamp) + smart_str(user.is_active)

account_activation_token = AccountActivationTokenGenerator()
