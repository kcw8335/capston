from django.contrib import admin
from .models import User_subinfo
from .models import Qrcode_info
from .models import Invitation

admin.site.register(User_subinfo)
admin.site.register(Qrcode_info)
admin.site.register(Invitation)