# Property constants
PROPERTY_STATUS_CHOICES = [
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('sold', 'Sold/Rented'),
    ('expired', 'Expired'),
]

LISTING_TYPE_CHOICES = [
    ('sale', 'For Sale'),
    ('rent', 'For Rent'),
    ('lease', 'For Lease'),
]

# User constants
USER_TYPE_CHOICES = [
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
    ('agent', 'Real Estate Agent'),
    ('admin', 'System Admin'),
]

# Transaction constants
TRANSACTION_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded'),
]

TRANSACTION_TYPE_CHOICES = [
    ('deposit', 'Deposit'),
    ('full_payment', 'Full Payment'),
    ('commission', 'Commission'),
    ('subscription', 'Subscription'),
]