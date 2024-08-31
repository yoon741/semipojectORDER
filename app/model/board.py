from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Board(Base):
    __tablename__ = 'board'

    bno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    userid: Mapped[str] = mapped_column(ForeignKey('member.userid'), index=True)  # 비식별관계
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    views: Mapped[int] = mapped_column(default=0)
    contents: Mapped[str]
    replys = relationship('Reply', back_populates='board') # 밑에 reply와 연결


class Reply(Base):
    __tablename__ = 'reply'

    rno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    reply: Mapped[str] = mapped_column(index=True)
    userid: Mapped[str] = mapped_column(ForeignKey('member.userid'), index=True)  # 비식별관계
    # regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))  # 초단위 수정
    bno: Mapped[int] = mapped_column(ForeignKey('board.bno'))
    rpno: Mapped[int] = mapped_column(ForeignKey('reply.rno'))
    board = relationship('Board', back_populates='replys') # 위에 board와 연결