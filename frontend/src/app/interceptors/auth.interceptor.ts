import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const token = authService.getToken();

  // اضافه کردن توکن به header
  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  // مدیریت خطاها
  return next(req).pipe(
    catchError((error) => {
      // اگر خطای 401 (Unauthorized) بود
      if (error.status === 401) {
        console.warn('⚠️ Interceptor: خطای 401 - توکن نامعتبر');

        // پاک کردن توکن و هدایت به لاگین
        localStorage.removeItem('access_token');
        router.navigate(['/login']);
      }

      return throwError(() => error);
    })
  );
};
