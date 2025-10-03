import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from './app.routes';
import { authInterceptor } from './interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    // تنظیمات Zone.js - اضافه کردن این خط
    provideZoneChangeDetection({
      eventCoalescing: true,
    }),

    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor])),
  ],
};
