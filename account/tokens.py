from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user_id, timestamp):
        return (
            text_type(user_id) + text_type(timestamp) 
        )

account_activation_token = AccountActivationTokenGenerator()