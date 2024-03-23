from django.db import models


class DeviceTypes(models.IntegerChoices):
    ANDROID_PHONE = 1, "Android Phone"
    LAPTOP = 2, "Laptop"
    I_PHONE = 3, "i Phone"
    I_PAD = 4, "i Pad"
    ANDROID_TAB = 5, "Android Tab"
    TV = 6, "TV"
    OTHER = 7, "Other"
