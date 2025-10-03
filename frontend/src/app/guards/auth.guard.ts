import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

/**
 * Guard برای محافظت از مسیرهای احراز هویت شده
 */
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  // بررسی توکن و وضعیت کاربر
  const token = authService.getToken();
  const user = authService.currentUser();

  // اگر توکن و کاربر موجود است
  if (token && user) {
    console.log('✅ Guard: کاربر احراز هویت شده - دسترسی مجاز');
    return true;
  }

  // اگر فقط توکن موجود است (کاربر هنوز لود نشده)
  if (token && !user) {
    console.log('⏳ Guard: توکن موجود است، در حال بارگذاری کاربر...');
    // اجازه دسترسی موقت (سرویس در حال بارگذاری کاربر است)
    return true;
  }

  // اگر احراز هویت نشده
  console.log('❌ Guard: دسترسی غیرمجاز - هدایت به صفحه لاگین');
  
  // ذخیره URL فعلی برای بازگشت بعد از لاگین
  router.navigate(['/login'], { 
    queryParams: { returnUrl: state.url } 
  });
  
  return false;
};
