import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'situ.settings')
django.setup()

from accounts.models import Cafe

# 기존 사용자 삭제 (필요시)
try:
    Cafe.objects.filter(cafe_id='store_001').delete()
except Cafe.DoesNotExist:
    pass

try:
    Cafe.objects.filter(cafe_id='store_002').delete()
except Cafe.DoesNotExist:
    pass

# 사용자 생성
user1 = Cafe.objects.create_user(cafe_id='store_001', cafe_name='카페파인', telephone='02-926-3726', password='0000')
user2 = Cafe.objects.create_user(cafe_id='store_002', cafe_name='빈트리', telephone='098-765-4321', password='1234')

# 비밀번호 확인
print(user1.cafe_id, user1.check_password('0000'))  # Should print True
print(user2.cafe_id, user2.check_password('1234'))       # Should print True