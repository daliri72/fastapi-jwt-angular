# استفاده از Python 3.12 به عنوان base image
FROM python:3.12-slim

# تنظیم متغیرهای محیطی
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تنظیم working directory
WORKDIR /app

# کپی فایل requirements
COPY requirements.txt .

# نصب dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# کپی کد پروژه
COPY . .

# باز کردن پورت 8000
EXPOSE 8000

# دستور اجرای برنامه
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
