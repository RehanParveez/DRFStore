from rest_framework.throttling import AnonRateThrottle

class Login(AnonRateThrottle):
    rate = '6/min'

class Refresh(AnonRateThrottle):
    rate = '9/min'