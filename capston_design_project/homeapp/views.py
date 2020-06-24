from django.contrib.auth.decorators import login_required
# 로그인을 했을 때만 실행되는 함수를 정의하기 위해 import
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
# 초대 메시지를 주고 받기 위해 import
from .models import Invitation

# 회원가입에서 이미지를 업로드하기 위해 import
from django.core.files.storage import FileSystemStorage
# 회원가입한 후 이미지를 가공하기 위해 import
from PIL import Image

# qrcode 생성을 위해 import
import qrcode

# qrcode를 생성하기 전 난수생성을 위해 import
import string
import random

# 아두이노 웹서버로 request를 보내기 위해 import - qrcodeid를 보냄
import requests

# 처음시작할 때 환영메시지를 띄우기 위한 함수
def login_show(request):
    return render(request, 'login.html', {'first':'true'})

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
            return render(request, 'login.html', {'error':'Please check your ID and Password!','id':id})
    # GET방식으로 요청이 들어올 때
    else:
        return render(request, 'login.html')

# GET방식일 때 회원가입 페이지 보여주는 함수
# POST방식일 때 회원가입 완료하는 함수
def signup(request):
    # method가 POST 방식일 때
    if request.method == "POST":
        if request.POST['overlap_alert'] == "true":    
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
            sub.availability = False
            
            # 얼굴사진
            # face_image = request.FILES['image']
            # face_image_file_name = name + "_얼굴사진.jpg"
            
            # # print(face_image_file_name)
            # # print(face_image) # 김창우.jpg
            # # print(type(face_image)) # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
            
            # fs = FileSystemStorage(location="media/images/")
            # filename = fs.save(face_image_file_name, face_image)
            
            # # print(face_image.name) # 김창우.jpg
            # # print(type(face_image.name)) # <class 'str'>
            # #print(filename) # 김창우.jpg
            # # print(type(filename)) # <class 'str'>
            # # uploaded_file_url = fs.url(filename)
            # # print(uploaded_file_url) # /media/%EA%B9%80%EC%B0%BD%EC%9A%B0.jpg
            # # print(type(uploaded_file_url)) # <class 'str'>
            
            # face_image_file_path = "images/" + filename
            # sub.face_image = face_image_file_path
            sub.save()

            # # 모바일에서 넘어온 이미지를 가공하여 저장
            # face_image_file_path = "C:/Users/kcw83/Desktop/capston_design_project/capston_design_project/media/images/" + filename
            # img = Image.open(face_image_file_path)
            # img = img.rotate(90)
            # img.save(face_image_file_path)

            # 회원가입에 성공했다면 가입축하 페이지로 이동
            if user is not None:
                return redirect('signup_congratulation')
        # 아이디 중복확인을 하지 않고 form이 들어올 때
        else :
            context = {
                'overlap_check':'',
                'overlap_alert':'false'
            }
            return render(request,'signup.html', context)
    # method가 GET 방식일 때
    else :
        context = {
            'overlap_alert':'',
            'overlap_check':''
        }
        return render(request, 'signup.html', context)

def signup_congratulation(request):
    return render(request, 'signup_congratulation.html')

# ID 중복확인하는 함수
def overlap(request, username):
    try:
        usernameC = str(User.objects.get(username=username))
        # 사용이 불가능한 아이디라면 이코드를 실행
        context = {
            'overlap_check':'false',
            'overlap_alert':''
        }
        return render(request, 'signup.html', context)
    except ObjectDoesNotExist:
        # 사용이 가능한 아이디라면 이 코드를 실행
        context = {
            'overlap_check':'true',
            'overlap_alert':'true',
            'id':username
        }
        return render(request, 'signup.html', context)

# IP_Address = "http://192.168.0.18
IP_Address = "http://172.20.10.2"

@login_required
def of(request):
    username = request.user.username
    print("username : ", username)
    pk = (User.objects.get(username = username)).pk
    availability = User_subinfo.objects.get(pk = pk).availability
    print(availability)
    # 로그인하고 of함수를 실행키기전에 전처리과정
    # 아두이노로 데이터 전송하고 데이터(잠금상태)를 받아와야함
    if availability == True:
        URL = IP_Address
        params = {'qrcode_id': 'status00000000000000'}
        response = requests.get(URL, params=params)
        r = response.text[63:69]
        print("r 값 : ", r)
        print(response.text)
        # r은 lock  , unlock 2개 중 한개의 메시지를 가져옴
        # 슬라이싱을 6개로 했으므로 lock 뒤에 공백 2개가 있음
        if r == "lock  ":
            lock = True
            unlock = False
        elif r == "unlock":
            lock = False
            unlock = True
        # access account list를 만드는 코드
        user_subinfo = User_subinfo.objects
        return render(request, 'of.html', {'lock':lock,'unlock':unlock,'availability':True,'user_subinfo':user_subinfo})
    else:
        try:
            inv = Invitation.objects.get(request_user = username)
            return render(request, 'of.html', {'availability':False, 'inv':inv})
        except ObjectDoesNotExist:
            return render(request, 'of.html', {'availability':False})

@login_required
def of_access_delete(request):
    username = request.POST.get('delete_user')
    if request.method == "POST" and username != "superuser":
        pk = (User.objects.get(username = username)).pk
        user = User_subinfo.objects.get(pk = pk)
        user.availability = False
        user.save()
        URL = IP_Address
        params = {'qrcode_id': 'status00000000000000'}
        response = requests.get(URL, params=params)
        r = response.text[63:69]
        print("r 값 : ", r)
        print(response.text)
        # r은 lock  , unlock 2개 중 한개의 메시지를 가져옴
        # 슬라이싱을 6개로 했으므로 lock 뒤에 공백 2개가 있음
        if r == "lock  ":
            lock = True
            unlock = False
        elif r == "unlock":
            lock = False
            unlock = True
        # access account list를 만드는 코드
        user_subinfo = User_subinfo.objects
        return render(request, 'of.html', {'lock':lock,'unlock':unlock,'availability':True,'user_subinfo':user_subinfo})
    elif request.method == "POST" and username == "superuser":
        URL = IP_Address
        params = {'qrcode_id': 'status00000000000000'}
        response = requests.get(URL, params=params)
        r = response.text[63:69]
        print("r 값 : ", r)
        print(response.text)
        # r은 lock  , unlock 2개 중 한개의 메시지를 가져옴
        # 슬라이싱을 6개로 했으므로 lock 뒤에 공백 2개가 있음
        if r == "lock  ":
            lock = True
            unlock = False
        elif r == "unlock":
            lock = False
            unlock = True
        # access account list를 만드는 코드
        user_subinfo = User_subinfo.objects
        return render(request, 'of.html', {'lock':lock,'unlock':unlock,'availability':True,'user_subinfo':user_subinfo,'superuser_no':'superuser_no'})
    else:
        return render(request, 'login.html')

@login_required
def of_accept_reject(request):
    username = request.user.username
    print(request.POST.get('accept_ok'))
    print(request.POST.get('reject_ok'))
    if request.method == "POST" and request.POST.get('accept_ok'):
        pk = (User.objects.get(username = username)).pk
        user_subinfo = User_subinfo.objects.get(pk = pk)
        user_subinfo.availability = True
        user_subinfo.save()
        # Invitation 삭제하기
        inv = Invitation.objects.get(request_user = username)
        inv.delete()
        # 상태 확인하기
        URL = IP_Address
        params = {'qrcode_id': 'status00000000000000'}
        response = requests.get(URL, params=params)
        r = response.text[63:69]
        print("r 값 : ", r)
        print(response.text)
        # r은 lock  , unlock 2개 중 한개의 메시지를 가져옴
        # 슬라이싱을 6개로 했으므로 lock 뒤에 공백 2개가 있음
        if r == "lock  ":
            lock = True
            unlock = False
        elif r == "unlock":
            lock = False
            unlock = True
        return render(request, 'of.html', {'lock':lock,'unlock':unlock,'availability':True})
    elif request.method == "POST" and request.POST.get('reject_ok'):
        # Invitation 삭제하기
        inv = Invitation.objects.get(request_user = username)
        inv.delete()
        return render(request, 'of.html', {'availability':False})
    else:
        return render(request, 'login.html')

@login_required
def of_search(request):
    search_name = request.POST['search_name']
    if request.method == "POST":
        try:
            get_username = User.objects.get(username = search_name).username
            # =============================================================================================
            username = request.user.username
            pk = (User.objects.get(username = username)).pk
            availability = User_subinfo.objects.get(pk = pk).availability
            URL = IP_Address
            params = {'qrcode_id': 'status00000000000000'}
            response = requests.get(URL, params=params)
            r = response.text[63:69]
            print("r 값 : ", r)
            print(response.text)
            # r은 lock  , unlock 2개 중 한개의 메시지를 가져옴
            # 슬라이싱을 6개로 했으므로 lock 뒤에 공백 2개가 있음
            if r == "lock  ":
                lock = True
                unlock = False
            elif r == "unlock":
                lock = False
                unlock = True
            user_subinfo = User_subinfo.objects
            return render(request, 'of.html', {'lock':lock,'unlock':unlock,'availability':True, 'message':get_username, 'send_button':True,'user_subinfo':user_subinfo})
        except ObjectDoesNotExist:
            # ===============================================================================================
            username = request.user.username
            pk = (User.objects.get(username = username)).pk
            availability = User_subinfo.objects.get(pk = pk).availability
            URL = IP_Address
            params = {'qrcode_id': 'status00000000000000'}
            response = requests.get(URL, params=params)
            r = response.text[63:69]
            print("r 값 : ", r)
            print(response.text)
            # r은 lock  , unlock 2개 중 한개의 메시지를 가져옴
            # 슬라이싱을 6개로 했으므로 lock 뒤에 공백 2개가 있음
            if r == "lock  ":
                lock = True
                unlock = False
            elif r == "unlock":
                lock = False
                unlock = True
            message = search_name + " can not be found!!"
            user_subinfo = User_subinfo.objects
            return render(request, 'of.html', {'lock':lock,'unlock':unlock,'availability':True,'message':message,'user_subinfo':user_subinfo})
    else:
        return render(request, 'login.html')

@login_required
def of_send_message(request):
    send_username = request.POST['send_username']
    if request.method == "POST":
        inv = Invitation()
        inv.send_user = request.user.username
        inv.request_user = send_username
        inv.save()
        username = request.user.username
        pk = (User.objects.get(username = username)).pk
        availability = User_subinfo.objects.get(pk = pk).availability
        URL = IP_Address
        params = {'qrcode_id': 'status00000000000000'}
        response = requests.get(URL, params=params)
        r = response.text[63:69]
        print("r 값 : ", r)
        print(response.text)
        # r은 lock  , unlock 2개 중 한개의 메시지를 가져옴
        # 슬라이싱을 6개로 했으므로 lock 뒤에 공백 2개가 있음
        if r == "lock  ":
            lock = True
            unlock = False
        elif r == "unlock":
            lock = False
            unlock = True
        # access account list를 만드는 코드
        user_subinfo = User_subinfo.objects
        return render(request, 'of.html', {'lock':lock,'unlock':unlock,'availability':True, 'send_ok':'send_ok','user_subinfo':user_subinfo})
    else:
        return render(request, 'login.html')    

@login_required
def of_lock(request):
    # 아두이노로 데이터 전송 -> 아두이노 잠금장치 잠김
    # POST 방식으로 request가 들어오고 잠금장치 상태가 열린상태라면 코드 실행
    # print(request.POST["lock"])
    # print(request.POST["unlock"])
    if request.method == "POST" and request.POST["unlock"] == "True":
        username = request.user.username
        pk = (User.objects.get(username = username)).pk
        availability = User_subinfo.objects.get(pk = pk).availability
        URL = IP_Address
        params = {'qrcode_id': 'lock0000000000000000'}
        response = requests.get(URL, params=params)
        # 아두이노의 상태를 확인한 후에 Locking status 사진 표시
        return render(request, 'of.html', {'lock':True,'unlock':False,'availability':True})
    # POST 방식으로 request가 들어오고 잠금장치 상태가 잠긴상태라면 코드 실행
    elif request.method == "POST" and request.POST["lock"] == "True":
        username = request.user.username
        pk = (User.objects.get(username = username)).pk
        availability = User_subinfo.objects.get(pk = pk).availability
        return render(request, 'of.html', {'lock':True,'unlock':False,'already_status':"lock",'availability':True})
    else:
        # GET 방식으로 request가 들어오면 무조건 login.html로 돌아가게 설정
        return render(request, 'login.html')

# def of_unlock(request):
#     if request.method == "POST":
#         return redirect('qrcode_function')
#     else:
#         # GET 방식으로 request가 들어오면 무조건 login.html로 돌아가게 설정
#         return render(request, 'login.html')

# def face_recognition(request):
#     if request.method == "POST":
#         return redirect('qrcode_function')
#     else:
#         return render(request, 'face_recognition.html')

@login_required
def qrcode_function(request):
    # POST 방식으로 request가 들어오고 잠긴 상태일 경우 코드 실행
    if request.method == "POST" and request.POST["lock"] == "True":
        # 누가 qrcode를 생성했는 지 알기 위한 username
        username = request.user.username
        name = User.objects.get(username = username).first_name
        
        # qrcode_id를 생성하기 위한 코드
        string_pool = string.ascii_letters + string.digits
        qrcode_id = ""
        for i in range(20):
            qrcode_id += random.choice(string_pool)
        
        # qrcode_id를 기반으로 qrcode 생성
        img = qrcode.make(qrcode_id)
        # 경로는 media의 qrcode username.jpg로 설정
        qrcode_image_upload_path = "media/qrcode/" + name + "_QRcode_이미지.jpg"
        # 이미지 저장
        img.save(qrcode_image_upload_path)
        
        # Qrcode_info 객체 생성 
        qrcode_object = Qrcode_info()
        qrcode_object.username = username
        qrcode_object.qrcode_id = qrcode_id
        qrcode_object.qrcode_image = "qrcode/"+ name + "_QRcode_이미지.jpg"
        # 데이터베이스에 저장
        qrcode_object.save()

        # 데이터베이스에서 username에 속하는 qrcode 이미지를 불러옴
        qrcode_info = Qrcode_info.objects.get(username = username)
        URL = IP_Address
        params = {'qrcode_id': qrcode_info.qrcode_id}
        requests.get(URL, params=params)
        return render(request, 'qrcode.html', {'qrcode_info':qrcode_info})
    # POST방식으로 request가 들어오고 열린 상태일 경우 코드 실행
    elif request.method == "POST" and request.POST["unlock"] == "True":
        return render(request, 'of.html', {'lock':False,'unlock':True,'already_status':"unlock",'availability':True})
    else :
        username = request.user.username
        print(username)
        qrcode_info = Qrcode_info.objects.get(username = username)
        qrcode_info.delete()
        return redirect('of')