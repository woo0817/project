from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout

# 1. 아이디 중복 확인 함수
def check_id(request):
    username = request.GET.get('username', None)
    is_taken = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'is_taken': is_taken})

# 2. 회원정보 저장 함수
def register_step2(request):
    if request.method == "POST":
        uid = request.POST.get('username')
        upw = request.POST.get('password')
        uname = request.POST.get('name')
        
        if not (uid and upw and uname):
            return render(request, 'policyapp/register_step2.html', {'error': '필수 항목을 입력해주세요.'})

        if User.objects.filter(username=uid).exists():
            return render(request, 'policyapp/register_step2.html', {'error': '이미 존재하는 아이디입니다.'})
        
        try:
            User.objects.create_user(username=uid, password=upw, last_name=uname)
            return redirect('login') 
        except Exception as e:
            return render(request, 'policyapp/register_step2.html', {'error': '가입 중 오류가 발생했습니다.'})
        
    return render(request, 'policyapp/register_step2.html')

# 3. 로그인 처리 함수
def id_login_view(request):
    if request.method == "POST":
        uid = request.POST.get('username')
        upw = request.POST.get('password')
        
        user = authenticate(request, username=uid, password=upw)
        
        if user is not None:
            login(request, user)
            # 로그인 성공 시 혹시 남아있을지 모를 비회원 세션 정리
            if request.session.get('is_guest'):
                request.session.flush()
                login(request, user) # 세션 초기화 후 다시 로그인 처리
            return redirect('index') 
        else:
            return render(request, 'policyapp/id_login.html', {'error': '아이디 또는 비밀번호가 틀렸습니다.'})
            
    return render(request, 'policyapp/id_login.html')

# 4. 비회원 로그인 처리 (이름 저장 및 상태 유지 추가)
def guest_login_view(request):
    if request.method == "POST":
        guest_name = request.POST.get('guest_name')
        # 비회원 인증 상태와 이름을 세션에 저장하여 브라우저 유지 동안 기억
        request.session['is_guest'] = True
        request.session['guest_name'] = guest_name
        return redirect('youth_home')
        
    return render(request, 'policyapp/guest_login.html')

# 5. 통합 로그아웃 함수 (회원 + 비회원 세션 모두 삭제)
def logout_view(request):
    auth_logout(request)           # Django 기본 회원 로그아웃
    request.session.flush()        # 비회원 세션 데이터(이름 등) 모두 삭제
    return redirect('index')       # 메인 페이지로 이동

# --- 나머지 페이지 함수 ---
def index(request):
    return render(request, 'policyapp/index.html')

def youth_home(request):
    # 세션 또는 유저 객체에서 이름만 추출하여 전달
    user_name = None
    if request.session.get('is_guest'):
        user_name = request.session.get('guest_name')
    elif request.user.is_authenticated:
        user_name = request.user.last_name if request.user.last_name else request.user.username
        
    return render(request, 'policyapp/youth_page.html', {'user_name': user_name})

def newlywed_home(request):
    return render(request, 'policyapp/newlywed_page.html')

def login_view(request):
    return render(request, 'policyapp/login.html')

def register_step1(request):
    if request.method == "POST":
        term1 = request.POST.get('term1')
        term2 = request.POST.get('term2')
        term_sub1 = request.POST.get('term_sub1')
        if term1 and term2 and term_sub1:
            return redirect('register_step2')
        else:
            return render(request, 'policyapp/register_step1.html', {'error': '필수 약관에 동의해주세요.'})
    return render(request, 'policyapp/register_step1.html')