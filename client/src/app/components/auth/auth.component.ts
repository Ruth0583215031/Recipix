// בס"ד - src/app/components/auth/auth.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { AuthService } from '../../auth.service'; // חובה שתי נקודות פעמיים!
import { Router } from '@angular/router';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.css'
})
export class AuthComponent {
  isLogin = true;
  authForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(6)]),
    user_name: new FormControl('')
  });

  constructor(private auth: AuthService, private router: Router) { }

  isInvalid(controlName: string): boolean {
    const control = this.authForm.get(controlName);
    return !!(control && control.invalid && (control.dirty || control.touched));
  }

  submit() {
    if (this.authForm.invalid) {
      this.authForm.markAllAsTouched();
      alert('חובה להזין אימייל תקין וסיסמה');
      return;
    }
    
    const val = this.authForm.value;
    
    if (this.isLogin) {
      this.auth.login(val).subscribe({
        next: () => this.router.navigate(['/profile']),
        error: () => alert('פרטי התחברות שגויים')
      });
    } else {
      if (!val.user_name) { alert('חובה שם משתמש'); return; }
      
      // כאן קו 49 מהטרמינל שלך - הפונקציה עכשיו תזוהה
      this.auth.register(val).subscribe({
        next: () => { 
          alert('נרשמת בהצלחה! כעת התחבר'); 
          this.isLogin = true; 
        },
        // פתרון לשגיאת ה-TS7006 (err implicitly has any type)
        error: (err: any) => alert(err.error?.error || 'שגיאה בהרשמה')
      });
    }
  }
}