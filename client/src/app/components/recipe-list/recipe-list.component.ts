// בס"ד - recipe-list.component.ts (גרסה מאוחדת ומתוקנת)
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { RecipeService } from '../../recipe.service';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-recipe-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './recipe-list.component.html',
  styleUrl: './recipe-list.component.css'
})
export class RecipeListComponent implements OnInit {
  recipes: any[] = [];
  isIngredientSearch = false;
  
  // משתני סינון
  selectedType: string = 'All';
  minRating: number = 0;
  currentSearch: string = '';

  constructor(private recipeService: RecipeService, private auth: AuthService) { }

  ngOnInit() { 
    this.fetchRecipes(); 
  }

  // פונקציה אחת מרכזית לכל סוגי הטעינה (בלי כפילויות!)
  fetchRecipes() {
    this.recipeService.getRecipes(this.currentSearch, this.selectedType, this.minRating)
      .subscribe({
        next: (data) => this.recipes = data,
        error: (err) => console.error('שגיאה בטעינה', err)
      });
  }

  toggleSearchMode() {
    this.isIngredientSearch = !this.isIngredientSearch;
    this.currentSearch = ''; // איפוס חיפוש במעבר מצב
    this.fetchRecipes();
  }

  onSearch(event: any) { 
    this.currentSearch = event.target.value;
    this.fetchRecipes(); 
  }

  onIngredientSearch(event: any) {
    const input = event.target.value;
    if (!input) { this.fetchRecipes(); return; }
    const ingredients = input.split(',').map((i: string) => i.trim());
    this.recipeService.searchByIngredients(ingredients).subscribe(data => this.recipes = data);
  }

  // פונקציות הסינון החדשות
  onTypeChange(event: any) {
    this.selectedType = event.target.value;
    this.fetchRecipes();
  }

  onRatingChange(rating: number) {
    // אם לוחצים על אותו דירוג שוב - זה מבטל את הסינון (חוזר ל-0)
    this.minRating = (this.minRating === rating) ? 0 : rating;
    this.fetchRecipes();
  }

  canDelete(recipeUserId: number): boolean {
    const user = this.auth.getUser();
    return !!user && (user.role === 'Admin' || user.id === recipeUserId);
  }

  deleteRecipe(id: number) {
    if (confirm('האם להעביר מתכון זה לארכיון?')) {
      this.recipeService.deleteRecipe(id).subscribe(() => {
        this.recipes = this.recipes.filter(r => r.id !== id);
      });
    }
  }
}