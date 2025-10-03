from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    کلاس تنظیمات برنامه که از فایل .env خوانده می‌شود
    """
    # کلید محرمانه برای JWT
    SECRET_KEY: str
    
    # الگوریتم رمزنگاری
    ALGORITHM: str
    
    # مدت زمان انقضای توکن
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # آدرس دیتابیس
    DATABASE_URL: str
    
    class Config:
        # مسیر فایل .env
        env_file = ".env"

settings = Settings()