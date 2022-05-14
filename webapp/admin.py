from .models import (
    Appointment, Applicant, Card,
    VFSAccount, CrawlAttempt, Settlement
                    )
from django.contrib import admin

admin.site.register(Applicant)
admin.site.register(Card)
admin.site.register(Appointment)
admin.site.register(VFSAccount)
admin.site.register(Settlement)
admin.site.register(CrawlAttempt)