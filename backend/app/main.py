# ایمپورت کتابخانه‌های FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# ایمپورت SQLAlchemy
from sqlalchemy.orm import Session

# ایمپورت datetime
from datetime import timedelta

# ایمپورت ماژول‌های داخلی
from .database import engine, get_db
from . import models, schemas, auth
from .dependencies import get_current_active_user
from .config import settings


# ایجاد جداول در دیتابیس
# این خط تمام مدل‌های تعریف شده را در دیتابیس ایجاد می‌کند
models.Base.metadata.create_all(bind=engine)


# ایجاد نمونه FastAPI
app = FastAPI(
    title="FastAPI JWT Authentication",
    description="سیستم احراز هویت JWT با FastAPI و Angular",
    version="1.0.0",
)


# تنظیمات CORS برای ارتباط با Angular
# این تنظیمات به فرانت‌اند اجازه می‌دهد به بک‌اند دسترسی داشته باشد
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # آدرس Angular
    allow_credentials=True,  # اجازه ارسال credentials
    allow_methods=["*"],  # اجازه تمام متدهای HTTP
    allow_headers=["*"],  # اجازه تمام headerها
)


@app.post("/api/auth/register", response_model=schemas.UserRegisterResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    ثبت‌نام کاربر جدید

    Args:
        user: اطلاعات کاربر جدید
        db: session دیتابیس

    Returns:
        اطلاعات کاربر ثبت شده

    Raises:
        HTTPException: اگر نام کاربری قبلاً ثبت شده باشد
    """
    # بررسی وجود نام کاربری در دیتابیس
    db_user = auth.get_user_by_username(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="نام کاربری قبلاً ثبت شده است")

    create_user = auth.create_user(db=db, user=user)

    # ایجاد کاربر جدید
    return {
        "username": create_user.username,
        "email": create_user.email,
        "full_name": create_user.full_name,
        "is_active": create_user.is_active,
    }


@app.post("/api/auth/login", response_model=schemas.Token)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    ورود کاربر و دریافت توکن JWT

    Args:
        login_data: اطلاعات ورود (نام کاربری و رمز عبور)
        db: session دیتابیس

    Returns:
        توکن JWT

    Raises:
        HTTPException: اگر نام کاربری یا رمز عبور اشتباه باشد
    """
    # احراز هویت کاربر
    user = auth.authenticate_user(db, login_data.username, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز عبور اشتباه است",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # تعیین مدت زمان اعتبار توکن
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # ایجاد توکن JWT
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # برگرداندن توکن
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user=Depends(get_current_active_user)):
    """
    دریافت اطلاعات کاربر فعلی
    این endpoint محافظت شده است و نیاز به توکن دارد

    Args:
        current_user: کاربر فعلی (از dependency)

    Returns:
        اطلاعات کاربر
    """
    return current_user


@app.get("/api/protected")
def protected_route(current_user=Depends(get_current_active_user)):
    """
    یک مسیر محافظت شده نمونه
    برای تست کارکرد احراز هویت

    Args:
        current_user: کاربر فعلی

    Returns:
        پیام خوش‌آمدگویی
    """
    return {
        "message": "این یک مسیر محافظت شده است",
        "user": current_user.username,
        "email": current_user.email,
    }


@app.get("/")
def root():
    """
    صفحه اصلی API

    Returns:
        پیام خوش‌آمدگویی
    """
    return {
        "message": "FastAPI با JWT Authentication",
        "docs": "/docs",
        "version": "1.0.0",
    }
