# ایمپورت کتابخانه‌های FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# ایمپورت کتابخانه JWT
from jose import JWTError, jwt

# ایمپورت SQLAlchemy
from sqlalchemy.orm import Session

# ایمپورت ماژول‌های داخلی
from .config import settings
from .database import get_db
from . import schemas, auth


# تعریف OAuth2 scheme که tokenUrl را مشخص می‌کند
# این URL باید با endpoint لاگین مطابقت داشته باشد
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),  # دریافت توکن از header
    db: Session = Depends(get_db)         # دریافت session دیتابیس
):
    """
    دریافت کاربر فعلی از روی توکن JWT
    این تابع به عنوان dependency در endpointهای محافظت شده استفاده می‌شود
    
    Args:
        token: توکن JWT از header درخواست
        db: session دیتابیس
    
    Returns:
        شیء کاربر فعلی
    
    Raises:
        HTTPException: اگر توکن نامعتبر باشد
    """
    # تعریف exception برای خطاهای احراز هویت
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="اعتبارسنجی توکن ناموفق بود",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # رمزگشایی توکن JWT
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # استخراج نام کاربری از payload
        username: str = payload.get("sub")
        
        # اگر نام کاربری وجود نداشت
        if username is None:
            raise credentials_exception
        
        # ایجاد شیء TokenData
        token_data = schemas.TokenData(username=username)
        
    except JWTError:
        # اگر خطایی در رمزگشایی رخ داد
        raise credentials_exception
    
    # جستجوی کاربر در دیتابیس
    user = auth.get_user_by_username(db, username=token_data.username)
    
    # اگر کاربر یافت نشد
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """
    بررسی اینکه کاربر فعلی فعال است یا خیر
    
    Args:
        current_user: کاربر فعلی از dependency قبلی
    
    Returns:
        شیء کاربر فعال
    
    Raises:
        HTTPException: اگر کاربر غیرفعال باشد
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=400, 
            detail="کاربر غیرفعال است"
        )
    return current_user
