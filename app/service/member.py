from sqlalchemy import insert, select, and_
import requests
from sqlalchemy.exc import SQLAlchemyError

from app.model.member import Member


class MemberService:
    @staticmethod
    def insert_member(db, member):
        try:
            stmt = insert(Member).values(
                userid=member.userid, passwd=member.passwd,
                name=member.name, email=member.email)
            result = db.execute(stmt)
            db.flush()   # 데이터베이스에 변경 사항을 즉시 반영하도록 하는 메서드
            db.commit()  # 정상처리될 경우 commit 후 return
            return result

        except SQLAlchemyError as ex:   # 예외처리 코드
            print(f'▶▶▶ insert_member 오류발생: {str(ex)}')
            db.rollback()      # 정상처리되지 않을 경우 rollback


    # google recaptcha 확인 url
    # https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
    @staticmethod
    def check_captcha(member):
        req_url = 'https://www.google.com/recaptcha/api/siteverify'
        params = { 'secret': '',
                   'response': member.captcha }
        res = requests.get(req_url, params=params)
        result = res.json()
        print('check => ', result)

        return result['success']
        # return True


    @staticmethod
    def login_member(db, data):
        try:   # 성공시 /routes/member.py에 loginok로 인해  myinfo페이지로 넘어감
            find_login = and_(Member.userid == data.get('userid'),
                              Member.passwd == data.get('passwd'))  # 테이블에 저장된 값과 일치하는지 확인
            stmt = select(Member.userid).where(find_login)  # find_login조건을 만족하는 값의 userid를 선택하는 쿼리문 생성
            result = db.execute(stmt).scalars().first()   # 쿼리를 실행하고, 첫번째 userid결과 값을 가져옴

            return result  # 유저아이디 반환

        except SQLAlchemyError as ex:
            print(f'login_member 오류 발생 : {str(ex)}')


    @staticmethod
    def selectone_member(db, userid):
        try:
            find_uid = Member.userid == userid
            stmt = select(Member).where(find_uid)
            result = db.execute(stmt).scalars()

            return result

        except SQLAlchemyError as ex:
            print(f'▷▷▷selectone_member 오류 발생 : {str(ex)}')