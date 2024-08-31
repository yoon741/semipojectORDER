import os
from datetime import datetime
from fastapi import Form
from app.schema.gallery import NewGallery

UPLOAD_PATH = 'C:/Java/nginx-1.26.2/html/cdn/img/'  # 저장경로


def get_gallery_data( title: str = Form(...),
            userid: str = Form(...), contents: str = Form(...)):
    return NewGallery(userid=userid, title=title, contents=contents)

async def process_upload(files):
    attachs = []  # 업로드된 파일정보를 저장하기 위해 리스트 생성
    today = datetime.today().strftime('%Y%m%d%H%M%S')  # UUID 생성 유니크한 고유식별코드
    # 내가올린 파일과 다른사람이 올린 파일이름이 같을 경우 겹치지 않기 위해 날짜시간 붙여서 생성
    for file in files:
        if file.filename != '' and file.size > 0:
            nfname = f'{today}{file.filename}'  # new file name
            # os.path.join(A,B) => A/B (경로생성 함수)
            fname = os.path.join(UPLOAD_PATH, nfname)   # 업로드할 파일경로 생성
            content = await file.read()     # 업로드할 파일의 내용을 비동기로 읽음
            with open(fname, 'wb') as f:    # 바이너리 형식으로 저장되어 기록됨
                f.write(content)    # 기록
            attach = [nfname, file.size]    # 업로드된 파일 정보를 리스트에 저장
            attachs.append(attach)

    return attachs

class GalleryService:
    pass