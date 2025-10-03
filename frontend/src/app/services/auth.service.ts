import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { Router } from '@angular/router';

import { User, LoginRequest, TokenResponse } from '../models/user.model';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly currentUserSignal = signal<User | null>(null);
  public readonly currentUser = this.currentUserSignal.asReadonly();

  public readonly isAuthenticated = computed(() => {
    return !!this.getToken() && !!this.currentUserSignal();
  });

  private readonly apiUrl = environment.apiUrl;

  constructor(private readonly http: HttpClient, private readonly router: Router) {
    console.log('🔧 AuthService: مقداردهی اولیه');
    this.initializeAuth();
  }

  /**
   * مقداردهی اولیه - بررسی توکن موجود
   */
  private initializeAuth(): void {
    const token = this.getToken();
    if (token) {
      console.log('🔑 AuthService: توکن موجود یافت شد - بارگذاری اطلاعات کاربر');
      this.loadCurrentUser();
    } else {
      console.log('❌ AuthService: توکن موجود نیست');
    }
  }

  /**
   * ورود کاربر
   */
  login(credentials: LoginRequest): Observable<TokenResponse> {
    console.log('🔐 AuthService: درخواست لاگین...');

    return this.http.post<TokenResponse>(`${this.apiUrl}/auth/login`, credentials).pipe(
      tap((response) => {
        console.log('✅ AuthService: لاگین موفق - ذخیره توکن');

        // ذخیره توکن
        this.setToken(response.access_token);

        // بارگذاری اطلاعات کاربر
        this.loadCurrentUser();
      })
    );
  }

  /**
   * خروج کاربر
   */
  logout(): void {
    console.log('🚪 AuthService: خروج کاربر');

    this.removeToken();
    this.currentUserSignal.set(null);
    this.router.navigate(['/login']);
  }

  /**
   * دریافت توکن
   */
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * ذخیره توکن
   */
  private setToken(token: string): void {
    localStorage.setItem('access_token', token);
    console.log('💾 AuthService: توکن ذخیره شد');
  }

  /**
   * حذف توکن
   */
  private removeToken(): void {
    localStorage.removeItem('access_token');
    console.log('🗑️ AuthService: توکن حذف شد');
  }

  /**
   * بارگذاری اطلاعات کاربر از API
   */
  private loadCurrentUser(): void {
    console.log('📥 AuthService: درخواست اطلاعات کاربر...');

    this.http.get<User>(`${this.apiUrl}/users/me`).subscribe({
      next: (user) => {
        console.log('✅ AuthService: اطلاعات کاربر دریافت شد:', user);
        this.currentUserSignal.set(user);
      },
      error: (error) => {
        console.error('❌ AuthService: خطا در بارگذاری کاربر:', error);

        // در صورت خطا، توکن را پاک می‌کنیم
        this.removeToken();
        this.currentUserSignal.set(null);

        // اگر خطای 401 باشد، به لاگین هدایت می‌کنیم
        if (error.status === 401) {
          this.router.navigate(['/login']);
        }
      },
    });
  }
}
