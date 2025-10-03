# ایمپورت کتابخانه‌های SQLAlchemy برای کار با دیتابیس
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# ایجاد Engine دیتابیس
# check_same_thread فقط برای SQLite لازم است
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# ایجاد SessionLocal برای ساخت session های دیتابیس
SessionLocal = sessionmaker(
    autocommit=False,  # تراکنش‌ها به صورت خودکار commit نمی‌شوند
    autoflush=False,   # داده‌ها به صورت خودکار flush نمی‌شوند
    bind=engine        # اتصال به engine
)

# کلاس پایه برای مدل‌های دیتابیس
Base = declarative_base()


def get_db():
    """
    تابع dependency برای دریافت session دیتابیس
    این تابع در هر درخواست، یک session جدید ایجاد می‌کند
    و پس از اتمام کار، آن را می‌بندد
    """
    db = SessionLocal()
    try:
        yield db  # session را برای استفاده برمی‌گرداند
    finally:
        db.close()  # پس از اتمام کار، session را می‌بندد
