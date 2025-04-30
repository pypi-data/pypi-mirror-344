from datetime import datetime
from typing import Optional
from sqlmodel import Field, MetaData, SQLModel

# 1. MetaData 객체 생성 시 schema 지정
#    (모든 테이블이 동일한 스키마를 공유할 경우)
SCHEMA_NAME = "cs2002"
metadata = MetaData(schema=SCHEMA_NAME)


class Base(SQLModel):
    metadata = metadata


class Wj(Base, table=True):
    __tablename__ = "wj"  # type: ignore

    wj_auto: Optional[int] = Field(
        default=None, primary_key=True, sa_column_kwargs={"autoincrement": "auto"}
    )
    wj_chart: str = Field(max_length=8)
    wj_suname: str = Field(max_length=50)
    wj_birthday: str = Field(max_length=8)


class Ns(Base, table=True):
    __tablename__ = "ns"  # type: ignore

    ns_auto: Optional[int] = Field(
        default=None, primary_key=True, sa_column_kwargs={"autoincrement": "auto"}
    )
    ns_chart: str = Field(max_length=8)
    ns_ymd: str = Field(max_length=50)
    ns_neyong1: str = Field()
    ns_neyong2: str = Field()
