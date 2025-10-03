# ایمپورت کتابخانه‌های Pydantic برای اعتبارسنجی داده‌ها
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    """
    اسکیمای پایه برای کاربر که شامل فیلدهای مشترک است
    """

    username: str
    email: EmailStr  # اعتبارسنجی خودکار فرمت ایمیل
    full_name: Optional[str] = None  # فیلد اختیاری


class UserCreate(UserBase):
    """
    اسکیمای ایجاد کاربر جدید
    برای دریافت اطلاعات از کلاینت هنگام ثبت‌نام
    """

    password: str  # رمز عبور به صورت متنی (قبل از هش)


class UserResponse(UserBase):
    """
    اسکیمای پاسخ کاربر
    برای ارسال اطلاعات کاربر به کلاینت
    """

    # id: int
    is_active: bool

    class Config:
        # اجازه خواندن داده از ORM models
        from_attributes = True


class Token(BaseModel):
    """
    اسکیمای پاسخ توکن JWT
    """

    access_token: str  # توکن دسترسی
    token_type: str  # نوع توکن (معمولاً "bearer")


class TokenData(BaseModel):
    """
    اسکیمای داده‌های داخل توکن
    """

    username: Optional[str] = None


class LoginRequest(BaseModel):
    """
    اسکیمای درخواست ورود
    برای دریافت اطلاعات لاگین از کلاینت
    """

    username: str
    password: str


# Schema جدید برای پاسخ ثبت‌نام (بدون ID)
class UserRegisterResponse(BaseModel):
    """
    اسکیمای پاسخ ثبت‌نام
    فقط اطلاعات عمومی و پیغام موفقیت را برمی‌گرداند
    """
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    message: str = "ثبت‌نام با موفقیت انجام شد"
    
    class Config:
        from_attributes = True