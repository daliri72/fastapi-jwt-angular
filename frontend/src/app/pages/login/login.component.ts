import { Component, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  FormBuilder, 
  FormGroup, 
  Validators, 
  ReactiveFormsModule 
} from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  private readonly fb = inject(FormBuilder);
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  
  readonly loginForm: FormGroup;
  readonly errorMessage = signal<string>('');
  readonly isLoading = signal<boolean>(false);

  constructor() {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
    
    // بررسی اینکه کاربر قبلاً لاگین کرده یا نه
    this.checkIfAlreadyLoggedIn();
  }

  /**
   * بررسی لاگین قبلی
   */
  private checkIfAlreadyLoggedIn(): void {
    if (this.authService.isAuthenticated()) {
      console.log('ℹ️ Login: کاربر قبلاً لاگین کرده - هدایت به داشبورد');
      this.router.navigate(['/dashboard']);
    }
  }

  /**
   * متد ارسال فرم لاگین
   */
  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    console.log('📤 Login: ارسال درخواست لاگین...');
    
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.authService.login(this.loginForm.value).subscribe({
      next: () => {
        console.log('✅ Login: لاگین موفق');
        this.isLoading.set(false);
        
        // دریافت URL بازگشت از query params
        const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/dashboard';
        console.log(`🔀 Login: هدایت به ${returnUrl}`);
        
        // تاخیر کوچک برای بارگذاری کامل اطلاعات کاربر
        setTimeout(() => {
          this.router.navigate([returnUrl]);
        }, 100);
      },
      error: (error) => {
        console.error('❌ Login: خطا در لاگین:', error);
        this.isLoading.set(false);
        
        const message = error.error?.detail || 'خطا در ورود به سیستم';
        this.errorMessage.set(message);
      }
    });
  }

  get username() {
    return this.loginForm.get('username');
  }

  get password() {
    return this.loginForm.get('password');
  }
}
