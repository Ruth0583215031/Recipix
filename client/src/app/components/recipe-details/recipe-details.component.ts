// בס"ד - recipe-details.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { RecipeService } from '../../recipe.service';
import { AuthService } from '../../auth.service'; // חובה לייבא
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-recipe-details',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './recipe-details.component.html',
  styleUrl: './recipe-details.component.css'
})
export class RecipeDetailsComponent implements OnInit {
  recipe: any = null;
  apiUrl = environment.apiUrl;

  constructor(
    private route: ActivatedRoute,
    public recipeService: RecipeService,
    public auth: AuthService // הזרקה כ-public פותרת את שגיאת ה-'auth does not exist'
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadRecipe(+id);
    }
  }

  loadRecipe(id: number) {
    this.recipeService.getRecipeById(id).subscribe({
      next: (data) => this.recipe = data,
      error: () => alert('המתכון לא נמצא')
    });
  }

  getVariationUrl(path: string): string {
    const pathPart = path.split('uploads')[1].replace(/\\/g, '/').replace(/^\/+/, '');
    return `${this.apiUrl}/uploads/${pathPart}`;
  }

  // מימוש הפונקציה שנקראת מה-HTML
  rateRecipe(score: number) {
    if (!this.recipe) return;
    this.recipeService.addRating(this.recipe.id, score).subscribe({
      next: () => {
        alert('תודה על הדירוג! ⭐');
        this.loadRecipe(this.recipe.id); // רענון הממוצע בתצוגה
      },
      error: (err) => {
        const msg = err.error?.error || 'שגיאה בשמירת הדירוג';
        alert(msg);
      }
    });
  }
}