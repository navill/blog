from storages.backends.s3boto3 import S3Boto3Storage


# S3Boto3Storage을 상속받아 기본 설정값을 오버라이드한다

class MediaStorage(S3Boto3Storage):
    # 업로드될 버킷 하위 폴더 이름
    location = ''  # 버킷이 분리되어 있기 때문에 별도의 폴더명이 없어도 된다.
    # 업로드될 버킷
    bucket_name = 'blog.media.navill.online'
    # 버킷이 존재하는 리전
    region_name = 'ap-northeast-2'

    # static과 동일한 경로가 검색되기 때문에 custom_domain을 설정해야한다.
    # 실제로 파일에 접속할 때 사용할 주소
    custom_domain = 's3.%s.amazonaws.com/%s' % (region_name, bucket_name)
    # custom_domain = bucket_name
    file_overwrite = False
