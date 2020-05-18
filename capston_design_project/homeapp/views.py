from django.shortcuts import render, redirect
# 로그인 함수를 사용하기 위해 import
from django.contrib import auth
# ID 중복확인을 위해 import
# 회원가입을 위해 import
from django.contrib.auth.models import User
# ID 중복확인을 위해 import 예외상황처리
from django.core.exceptions import ObjectDoesNotExist

# 회원가입을 위해 import
from .models import User_subinfo
# qrcode 데이터베이스를 사용하기 위해 import
from .models import Qrcode_info

# 회원가입에서 이미지를 업로드하기 위해 import
from django.core.files.storage import FileSystemStorage

# qrcode 생성을 위해 import
import qrcode
from PIL import Image

# qrcode를 생성하기 전 난수생성을 위해 import
import string
import random

# 로그인 기능 구현
def login(request):
    # POST방식으로 요청이 들어올 떄
    if request.method == "POST":
        id = request.POST['id']
        pw = request.POST['pw']
        user = auth.authenticate(request, username=id, password=pw)
        # 로그인에 성공할 때
        if user is not None:
            auth.login(request, user)
            return redirect('of')
        # 로그인에 실패할 때
        else:
            return render(request, 'login.html', {'error':'아이디와 비밀번호를 확인해주세요!','id':id})
    # GET방식으로 요청이 들어올 때
    else:
        return render(request, 'login.html', {'first':"True"})

# GET방식일 때 회원가입 페이지 보여주는 함수
# POST방식일 때 회원가입 완료하는 함수
def signup(request):
    if request.method == "POST":
        if request.POST['overlap'] == "사용 가능한 아이디입니다.":    
            username = request.POST['username']
            password = request.POST['password']
            name = request.POST['name']
            email = request.POST['email']
            user = User.objects.create_user(username, email=email, password=password)
            user.last_name = name
            user.first_name = name
            user.save()
            pk = (User.objects.get(username=username)).pk
            # 객체 생성
            sub = User_subinfo()
            # 외래키 저장
            sub.username = User.objects.get(pk=pk)
            sub.usernameC = username
            # 주민번호
            r = request.POST['registration1'] + "-" + request.POST['registration2']
            sub.resident_registration_number = r
            # 면허증번호
            d = request.POST['license1'] + "-" + request.POST['license2'] + "-" + request.POST['license3'] + "-" + request.POST['license4']
            sub.driver_license = d
            
            # 얼굴사진
            face_image = request.FILES['image']
            # print(face_image) # 김창우.jpg
            # print(type(face_image)) # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
            fs = FileSystemStorage(location="media/images/")
            filename = fs.save(face_image.name, face_image)
            # print(face_image.name) # 김창우.jpg
            # print(type(face_image.name)) # <class 'str'>
            # print(filename) # 김창우.jpg
            # print(type(filename)) # <class 'str'>
            uploaded_file_url = fs.url(filename)
            # print(uploaded_file_url) # /media/%EA%B9%80%EC%B0%BD%EC%9A%B0.jpg
            # print(type(uploaded_file_url)) # <class 'str'>

            # 여기가 애매함 다시 시작
            sub.face_image = uploaded_file_url
            sub.save()
            # 회원가입에 성공했다면 가입축하 페이지로 이동
            if user is not None:
                return redirect('signup_congratulation')
        else :

            context = {}
            return render(request,'signup.html',{'overlap_check':'false', 'alert':'아이디 중복을 확인해주세요.'})
    else :
        return render(request, 'signup.html', {'alert':'아이디 중복을 확인해주세요.'})

def signup_congratulation(request):
    return render(request, 'signup_congratulation.html')

# ID 중복확인하는 함수
def overlap(request, username):
    try:
        usernameC = str(User.objects.get(username=username))
        return render(request, 'signup.html', {'alert':'사용 불가능한 아이디입니다.'})
    except ObjectDoesNotExist:
        return render(request, 'signup.html', {'alert':'사용 가능한 아이디입니다.','id':username})


def of(request):
    # 로그인하고 of함수를 실행키기전에 전처리과정 필요
    # 아두이노로 데이터 전송하고 데이터(잠금상태)를 받아와야함
    # 지금의 경우는 lock을 기본으로 데이터 전송함
    return render(request, 'of.html', {'lock':True,'unlock':False})

def of_lock(request):
    # 아두이노로 데이터 전송 -> 아두이노 잠금장치 잠김
    # 아두이노의 상태를 확인한 후에 Locking status 사진 표시
    return render(request, 'of.html', {'lock':True,'unlock':False})

def of_unlock(request):
    return redirect('face_recognition')
    # return render(request, 'of.html', {'lock':False,'unlock':True})

def face_recognition(request):
    if request.method == "POST":
        return redirect('qrcode_function')
    else:
        return render(request, 'face_recognition.html')

def qrcode_function(request):
    if request.method == "POST":
        # 누가 qrcode를 생성했는 지 알기 위한 username
        username = request.user.username
        
        # qrcode_id를 생성하기 위한 코드
        string_pool = string.ascii_letters + string.digits + string.punctuation
        qrcode_id = ""
        for i in range(20):
            qrcode_id += random.choice(string_pool)
        
        # qrcode_id를 기반으로 qrcode 생성
        img = qrcode.make(qrcode_id)
        # 경로는 media의 qrcode username.jpg로 설정
        qrcode_image_upload_path = "media/qrcode/"+ username + ".jpg"
        # 이미지 저장
        img.save(qrcode_image_upload_path)
        
        # Qrcode_info 객체 생성 
        qrcode_object = Qrcode_info()
        qrcode_object.username = username
        qrcode_object.qrcode_id = qrcode_id
        qrcode_object.qrcode_image = "qrcode/"+ username + ".jpg"
        # 데이터베이스에 저장
        qrcode_object.save()

        # 데이터베이스에서 username에 속하는 qrcode 이미지를 불러옴
        qrcode_info = Qrcode_info.objects.get(username = username)
        return render(request, 'qrcode.html', {'qrcode_info':qrcode_info})
    else :
        username = request.user.username
        qrcode_info = Qrcode_info.objects.get(username = username)
        qrcode_info.delete()
        return redirect('of')

# 아두이노에서 호출하는 함수
def qrcode_GET(request, username):
    try:
        qrcode_info = Qrcode_info.objects.get(username = username)
        return render(request, 'qrcode_GET.html', {'qrcode_id':qrcode_info.qrcode_id})
    except ObjectDoesNotExist:
        return render(request, 'qrcode_GET.html', {'qrcode_id':'00000000000000000000'})