from django.db import models
from django.contrib.auth.models import User

# media 파일에 있는 qrcode 파일을 보안상의 이유로 삭제하기위해 import
import os
from django.conf import settings

class User_subinfo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    usernameC = models.CharField(max_length=30, null=True)
    # 주민번호
    resident_registration_number = models.CharField(max_length=30)
    # 면허증번호
    driver_license = models.CharField(max_length=50)
    # 제어 가능 여부
    availability = models.BooleanField(default=False)

    # 이미지
    # face_image = models.ImageField(upload_to='images/', null=True)

    # admin 페이지에 usernameC가 보이도록 설정
    def __str__(self):
        return self.usernameC

    # media 파일을 삭제하기 위해 delete 메소드를 오버라이딩
    def delete(self, *args, **kargs):
        if self.face_image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.face_image.path))
        super(User_subinfo, self).delete(*args, **kargs)

class Invitation(models.Model):
    # 초대메시지를 보내는 사람
    send_user = models.CharField(max_length=30)
    # 초대메시지를 받는 사람
    request_user = models.CharField(max_length=30)


# qrcode를 저장하기 위한 데이터베이스
class Qrcode_info(models.Model):
    # 어떤 사람이 qrcode를 저장했는 지 알기 위한 필드
    username = models.CharField(max_length=30, null=False)
    # qrcode 이미지를 저장하기 위한 필드
    qrcode_image = models.ImageField(upload_to='qrcode/', null=False)
    # 랜덤으로 문자 및 숫자를 생성하여 qrcode_id 저장
    qrcode_id = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.username

    # media 파일을 삭제하기 위해 delete 메소드를 오버라이딩
    def delete(self, *args, **kargs):
        if self.qrcode_image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.qrcode_image.path))
        super(Qrcode_info, self).delete(*args, **kargs)

