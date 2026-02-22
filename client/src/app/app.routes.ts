// בס"ד - app.routes.ts
import { Routes } from '@angular/router';
import { RecipeListComponent } from './components/recipe-list/recipe-list.component';
import { AuthComponent } from './components/auth/auth.component';
import { ProfileComponent } from './components/profile/profile.component';
import { RecipeDetailsComponent } from './components/recipe-details/recipe-details.component';
import { authGuard } from './auth.guard';

export const routes: Routes = [
  { path: '', component: RecipeListComponent }, // דף הבית - רשימה מינימליסטית
  { path: 'login', component: AuthComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [authGuard] },
  { path: 'recipe/:id', component: RecipeDetailsComponent }, // דף מתכון יחיד
  { path: '**', redirectTo: '' }
];