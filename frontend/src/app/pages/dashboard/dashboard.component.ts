import { Component, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

/**
 * کامپوننت داشبورد
 */
@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  // استفاده از inject() برای دریافت سرویس
  private readonly authService = inject(AuthService);
  
  // حالا می‌توانیم از authService استفاده کنیم
  readonly currentUser = this.authService.currentUser;
  
  // Computed signal برای نام نمایشی
  readonly displayName = computed(() => {
    const user = this.currentUser();
    return user?.full_name || user?.username || 'کاربر';
  });

  /**
   * متد خروج از سیستم
   */
  logout(): void {
    if (confirm('آیا مطمئن هستید که می‌خواهید خارج شوید؟')) {
      this.authService.logout();
    }
  }
}
