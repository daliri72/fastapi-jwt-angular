import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  // مسیر اصلی - هدایت به dashboard
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full',
  },

  // صفحه لاگین - بدون Guard
  {
    path: 'login',
    component: LoginComponent,
    title: 'ورود به سیستم',
  },

  // داشبورد - با Guard محافظت شده
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [authGuard], // ✅ Guard اینجا فعال است
    title: 'داشبورد',
  },

  // مسیرهای نامعتبر - هدایت به لاگین
  {
    path: '**',
    redirectTo: '/login',
  },
];
