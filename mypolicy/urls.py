"""
URL configuration for mypolicy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
# 기존에 에러가 나고 있을 코드 예시:
# from mypolicy import views  <-- 이렇게 되어 있다면 에러가 날 수 있습니다.

# 수정 권장 코드:
from policyapp import views  # 같은 폴더에 있는 views.py를 가져옵니다.
urlpatterns = [
    # admin.site.手 -> admin.site.urls 로 수정!
    path('admin/', admin.site.urls), 
    path('', views.index, name='index'),
    path('youth/', views.youth_home, name='youth_home'),
    path('newlywed/', views.newlywed_home, name='newlywed_home'),
    path('login/', views.login_view, name='login'),
    path('login/id/', views.id_login_view, name='id_login'),
    path('login/guest/', views.guest_login_view, name='guest_login'),
    path('register/', views.register_step1, name='register_step1'),  # name 설정 확인!
    path('register/step2/', views.register_step2, name='register_step2'),
    path('register/step2/', views.register_step2, name='register_step2'),
    path('check-id/', views.check_id, name='check_id'),
path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
path('logout/', views.logout_view, name='logout'),
]



