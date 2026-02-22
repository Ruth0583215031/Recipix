import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../auth.service';
import { User } from '../../models/user.model';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  currentUser: User | null = null;

  constructor(public auth: AuthService) {
    // מאזין לשינויים ב-Service ומעדכן את התצוגה בזמן אמת
    this.auth.user$.subscribe(user => {
      this.currentUser = user;
    });
  }

  // הפונקציה שהייתה חסרה ב-TypeScript וגרמה לשגיאה ב-HTML
  getUserName(): string {
    return this.currentUser?.user_name || '';
  }

  // פונקציית התנתקות
  onLogout() {
    this.auth.logout();
  }
}