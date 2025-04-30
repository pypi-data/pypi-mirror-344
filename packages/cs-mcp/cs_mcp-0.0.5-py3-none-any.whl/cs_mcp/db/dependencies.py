from contextlib import asynccontextmanager
import logging
from typing import Annotated, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from cs_mcp.configs import config


# SQLAlchemy 로깅 설정 수정
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# 중복 로깅 방지를 위해 propagate 설정 비활성화
logging.getLogger("sqlalchemy.engine").propagate = False

engine = create_async_engine(
    config.DATABASE_URL,
    echo=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# 의존성 주입을 위한 비동기 세션 제공자 with 문으로 사용할 수 있게

@asynccontextmanager
async def get_asession() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            print(f"💡[ 세션 생성 완료 ] {session}")
            yield session
            await session.commit()
            print(f"💡[ 세션 커밋 완료 ] {session}")
        except SQLAlchemyError as e:
            print(f"🚨[ DB 오류, 롤백 ] {e}")
            await session.rollback()
            # 프로덕션에서는 에러 로깅 후 적절한 HTTPException 발생 고려

        except Exception as e:
            print(f"🚨[ 예외 발생, 롤백 ] {e}")
            await session.rollback()
            raise  # 원래 예외 다시 발생
        finally:
            await session.close()
            print(f"💡[ 세션 종료 ] {session}")
