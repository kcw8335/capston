from django.contrib import admin
from django.urls import path
import homeapp.views
# media를 사용하기 위해 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeapp.views.login, name='login'),
    path('signup/', homeapp.views.signup, name='signup'),
    path('signup_congratulation/', homeapp.views.signup_congratulation, name="signup_congratulation"),
    path('overlap/<username>', homeapp.views.overlap, name="overlap"),

    path('of/', homeapp.views.of, name="of"),
    path('of/lock/', homeapp.views.of_lock, name="of_lock"),
    path('of/unlock/', homeapp.views.of_unlock, name="of_unlock"),

    path('face_recognition/', homeapp.views.face_recognition, name="face_recognition"),
    path('qrcode_function/', homeapp.views.qrcode_function, name="qrcode_function"),

    path('qrcode_GET/<username>', homeapp.views.qrcode_GET, name="qrcode_GET"),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)