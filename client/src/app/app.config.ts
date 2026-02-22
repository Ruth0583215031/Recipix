// app.config.ts מעודכן
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http'; // עדכון הייבוא
import { authInterceptor } from './interceptors/auth.interceptor'; // ייבוא ה-interceptor
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }), 
    provideRouter(routes),
    // הוספת ה-Interceptor למערך ה-Interceptors
    provideHttpClient(withInterceptors([authInterceptor])) 
  ]
};