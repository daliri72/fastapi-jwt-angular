# ایمپورت انواع ستون‌های دیتابیس
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class User(Base):
    """
    مدل کاربر در دیتابیس
    این کلاس نشان‌دهنده جدول users در دیتابیس است
    """

    # نام جدول در دیتابیس
    __tablename__ = "users"

    # شناسه یکتای کاربر (کلید اصلی)
    id = Column(Integer, primary_key=True, index=True)

    # نام کاربری (یکتا و قابل جستجو)
    username = Column(String, unique=True, index=True, nullable=False)

    # ایمیل کاربر (یکتا و قابل جستجو)
    email = Column(String, unique=True, index=True, nullable=False)

    # نام کامل کاربر (اختیاری)
    full_name = Column(String)

    # رمز عبور هش شده
    hashed_password = Column(String, nullable=False)

    # وضعیت فعال بودن کاربر
    is_active = Column(Boolean, default=True)
