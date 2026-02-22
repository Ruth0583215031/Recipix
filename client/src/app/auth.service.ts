// בס"ד - src/app/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, BehaviorSubject } from 'rxjs';
import { User } from './models/user.model';
import { environment } from './environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private userSubject = new BehaviorSubject<User | null>(this.getUserFromStorage());
  user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient) { }

  private getUserFromStorage(): User | null {
    const data = localStorage.getItem('user');
    try { return data ? JSON.parse(data) : null; } catch { return null; }
  }

  getToken(): string | null { return localStorage.getItem('token'); }
  getUser(): User | null { return this.userSubject.value; }
  isLoggedIn(): boolean { return !!this.userSubject.value; }

  login(credentials: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, credentials).pipe(
      tap(res => {
        localStorage.clear();
        localStorage.setItem('token', res.token);
        localStorage.setItem('user', JSON.stringify(res.user));
        this.userSubject.next(res.user);
      })
    );
  }

  // --- הפונקציה שהייתה חסרה וגרמה לשגיאה בטרמינל ---
  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, userData);
  }

  logout() {
    localStorage.clear();
    this.userSubject.next(null);
    window.location.href = '/login';
  }

  refreshStatus(id: number): Observable<Partial<User>> {
    return this.http.get<Partial<User>>(`${this.apiUrl}/user_status/${id}`).pipe(
      tap(res => {
        const current = this.userSubject.value;
        if (current) {
          const updated = { ...current, ...res };
          localStorage.setItem('user', JSON.stringify(updated));
          this.userSubject.next(updated);
        }
      })
    );
  }

  // --- פונקציות ניהול ---
  getAllUsers(): Observable<any[]> { return this.http.get<any[]>(`${this.apiUrl}/admin/users`); }
  getAdminRequests(): Observable<any[]> { return this.http.get<any[]>(`${this.apiUrl}/admin/requests`); }
  approveUser(userId: number): Observable<any> { return this.http.post(`${this.apiUrl}/admin/approve_user/${userId}`, {}); }
  sendUpgradeRequest(userId: number): Observable<any> { return this.http.post(`${this.apiUrl}/request_upgrade`, { user_id: userId }); }
}