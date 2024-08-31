import os
from datetime import datetime
from fastapi import Form
from sqlalchemy import insert, select, distinct, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased, joinedload

from app.model.product import Product, PrdAttach
from app.schema.product import ProductCreate

UPLOAD_PATH = 'C:/Java/img/'  # 저장경로


def get_product_data( title: str = Form(...),
                      userid: str = Form(...), contents: str = Form(...)):
    return ProductCreate(userid=userid, title=title, contents=contents)

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

class ProductService:
    @staticmethod
    def insert_product(prd, attachs, db):
        try:
            stmt = insert(Product).values(userid=prd.userid,
                                          title=prd.title, contents=prd.contents)
            result = db.execute(stmt)  #인서트된 글번호를

            # 방금 생성한 레코드의 기본키 값 : inserted_primary_key
            inserted_prdno = result.inserted_primary_key[0]
            for attach in attachs:
                data = {'fname': attach[0], 'fsize': attach[1],
                        'prdno': inserted_prdno}  # 글번호가 만들어져야만
                stmt = insert(PrdAttach).values(data)
                result = db.execute(stmt)

            db.commit()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_product!!에서 오류발생 : {str(ex)}')
            db.rollback()


    @staticmethod
    def select_product(cpg, db):
        #  select distinct g.gno, title, userid, g.regdate, views,
        #  first_value(fname) over (partition by g.gno) fname
        #  from gallery g join galattach ga
        #  on g.gno = ga.gno order by g.gno desc;
        try:
            stmt = select(distinct(Product.prdno).label('prdno'),
                          Product.title, Product.userid,
                          Product.regdate, Product.views,
                          func.first_value(PrdAttach.fname) \
                          .over(partition_by=Product.prdno).label('fname')) \
                .join_from(Product, PrdAttach) \
                .order_by(Product.prdno.desc()).limit(25)
            result = db.execute(stmt)

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_product에서 오류발생 : {str(ex)}')
            db.rollback()


    @staticmethod
    def selectone_product(prdno, db):
        try:
            stmt = select(Product).options(joinedload(Product.attachs)) \
                .where(Product.prdno == prdno)
            result = db.execute(stmt).scalars().first()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_product에서 오류발생 : {str(ex)}')
            db.rollback()