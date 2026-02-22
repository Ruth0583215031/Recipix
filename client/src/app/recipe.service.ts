// בס"ד - recipe.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from './environments/environment';

@Injectable({ providedIn: 'root' })
export class RecipeService {
  private apiUrl = `${environment.apiUrl}/recipes`;

  constructor(private http: HttpClient) { }

  getRecipes(searchTerm: string = '', type: string = '', minRating: number = 0): Observable<any[]> {
    let params = new HttpParams();
    if (searchTerm) params = params.set('search', searchTerm);
    if (type && type !== 'All') params = params.set('type', type);
    if (minRating > 0) params = params.set('min_rating', minRating.toString());

    return this.http.get<any[]>(`${this.apiUrl}/`, { params });
  }

  getRecipeById(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  addRecipe(formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/add_recipe`, formData);
  }

  deleteRecipe(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete_recipe/${id}`);
  }

  // אלגוריתם חיפוש לפי רכיבים
  searchByIngredients(ingredients: string[]): Observable<any[]> {
    return this.http.post<any[]>(`${this.apiUrl}/search_by_ingredients`, { ingredients });
  }

  // ניהול ארכיון למנהלים
  getArchivedRecipes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/archived`);
  }

  restoreRecipe(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/restore_recipe/${id}`, {});
  }

  addRating(recipeId: number, score: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/rate`, { recipe_id: recipeId, score });
  }
}
