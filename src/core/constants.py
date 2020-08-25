from django.utils.translation import gettext as _

class Messages:
    NO_PERMISSION = {
        'message': _('You don\'t have the permission to perform this action'),
        'code': 'no_permission'
    }

    INVALID_DISCOUNT_CODE = {
        'message': _('This discount code is invalid'),
        'code': 'invalid_discount_code'
    }

    MISSING_BILLING_ADDRESS = {
        'message': _('Billing address is missing'),
        'code': 'missing_billing_address'
    }
    