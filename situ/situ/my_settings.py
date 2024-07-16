DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'situ',#db명
        'USER': 'sehyeon', #db user 이름
        'PASSWORD': 'rlatpgus', #db password
        'HOST': 'localhost', #나중에 aws로 연결
        'PORT': '3306', #mysql 포트번호
    }
}