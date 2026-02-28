from rest_framework.throttling import AnonRateThrottle

class Login(AnonRateThrottle):
    rate = '4/min'

class Refresh(AnonRateThrottle):
    rate = '8/min'