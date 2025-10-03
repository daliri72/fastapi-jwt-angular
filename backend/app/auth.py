from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .config import settings
from . import models, schemas   

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    بررسی صحت رمز عبور وارد شده با رمز عبور هش شده
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    هش کردن رمز عبور
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    ایجاد توکن JWT با داده‌های مشخص
    
    Args:
        data: دیکشنری حاوی داده‌های مورد نظر برای قرار دادن در توکن
        expires_delta: مدت زمان اعتبار توکن (اختیاری)
    
    Returns:
        توکن JWT رمزنگاری شده
    """
    # کپی از داده‌های ورودی
    to_encode = data.copy()
    
    # تعیین زمان انقضا
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # اضافه کردن زمان انقضا به داده‌ها
    to_encode.update({"exp": expire})
    
    # رمزنگاری و ایجاد توکن
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str):
    """
    احراز هویت کاربر با نام کاربری و رمز عبور
    
    Args:
        db: session دیتابیس
        username: نام کاربری
        password: رمز عبور
    
    Returns:
        شیء کاربر اگر احراز هویت موفق باشد، در غیر این صورت False
    """
    # جستجوی کاربر در دیتابیس
    user = db.query(models.User).filter(models.User.username==username).first()
    
    # اگر کاربر یافت نشد
    if not user:
        return False
    
    # اگر رمز عبور اشتباه است
    if not verify_password(password, user.hashed_password):
        return False
    
    # برگرداندن کاربر
    return user


def get_user_by_username(db: Session, username: str):
    """
    دریافت کاربر از دیتابیس با نام کاربری
    
    Args:
        db: session دیتابیس
        username: نام کاربری
    
    Returns:
        شیء کاربر یا None
    """
    return db.query(models.User).filter(
        models.User.username == username
    ).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    ایجاد کاربر جدید در دیتابیس
    
    Args:
        db: session دیتابیس
        user: داده‌های کاربر جدید
    
    Returns:
        شیء کاربر ایجاد شده
    """
    # هش کردن رمز عبور
    hashed_password = get_password_hash(user.password)
    
    # ایجاد شیء کاربر
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active = True
    )
    
    # اضافه کردن به دیتابیس
    db.add(db_user)
    
    # ذخیره تغییرات
    db.commit()
    
    # بازخوانی کاربر از دیتابیس
    db.refresh(db_user)
    
    return db_user