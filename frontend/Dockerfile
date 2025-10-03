# مرحله Build
FROM node:20-alpine AS builder

WORKDIR /app

# کپی package files
COPY package*.json ./

# نصب همه dependencies (بدون --only=production)
RUN npm ci && npm cache clean --force

# کپی کد پروژه
COPY . .

# Build برای production
RUN npm run build -- --configuration=production

# مرحله Production با Nginx
FROM nginx:alpine

# حذف تنظیمات پیش‌فرض nginx
RUN rm -rf /usr/share/nginx/html/*

# کپی فایل‌های build شده از مرحله قبل
COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html

# کپی تنظیمات nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# باز کردن پورت 80
EXPOSE 80

# دستور اجرا
CMD ["nginx", "-g", "daemon off;"]
