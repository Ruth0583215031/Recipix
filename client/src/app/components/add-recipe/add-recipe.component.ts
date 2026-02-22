// בס"ד - add-recipe.component.ts המעודכן
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl, Validators, FormArray } from '@angular/forms';
import { RecipeService } from '../../recipe.service'; 

@Component({
  selector: 'app-add-recipe',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './add-recipe.component.html',
  styleUrl: './add-recipe.component.css'
})
export class AddRecipeComponent {
  recipeForm = new FormGroup({
    name: new FormControl('', [Validators.required, Validators.minLength(3)]),
    type: new FormControl('Dairy', Validators.required),
    instructions: new FormControl('', [Validators.required, Validators.minLength(10)]),
    ingredients: new FormArray([this.createIngredientGroup()])
  });

  selectedFile: File | null = null;

  constructor(private recipeService: RecipeService) {}

  createIngredientGroup() {
    return new FormGroup({
      amount: new FormControl(1, [Validators.required, Validators.min(0.1)]),
      unit: new FormControl('יחידות', Validators.required),
      product: new FormControl('', [Validators.required, Validators.minLength(2)])
    });
  }

  get ingredients() { return this.recipeForm.get('ingredients') as FormArray; }
  
  addIngredient() { 
    this.ingredients.push(this.createIngredientGroup()); 
  }

  removeIngredient(index: number) { 
    if (this.ingredients.length > 1) {
      this.ingredients.removeAt(index); 
    }
  }

  onFileSelect(event: any) { 
    this.selectedFile = event.target.files[0]; 
  }

  isInvalid(controlName: string, index?: number): boolean {
    let control;
    if (index !== undefined) {
      control = this.ingredients.at(index).get(controlName);
    } else {
      control = this.recipeForm.get(controlName);
    }
    // החזרת אמת אם השדה לא תקין ובוצע ניסיון שליחה או נגיעה
    return !!(control && control.invalid && (control.dirty || control.touched));
  }

  onSubmit() {
    // שלב 1: בדיקת תקינות מלאה כולל קובץ
    if (this.recipeForm.invalid || !this.selectedFile) {
      // הפעלת מצב "נגעו בשדה" לכל השדות בבת אחת - זה מה שמציג את השגיאות באדום
      this.recipeForm.markAllAsTouched();
      this.ingredients.markAllAsTouched();
      
      let errorDetails = 'לא ניתן לשמור את המתכון:\n';
      if (!this.selectedFile) errorDetails += '- חובה לצרף תמונה למתכון\n';
      if (this.recipeForm.get('name')?.invalid) errorDetails += '- שם המתכון קצר מדי או חסר\n';
      if (this.recipeForm.get('instructions')?.invalid) errorDetails += '- הוראות ההכנה חייבות להכיל 10 תווים לפחות\n';
      if (this.ingredients.invalid) errorDetails += '- וודא שכל המצרכים מולאו (כמות ושם מוצר)\n';
      
      alert(errorDetails);
      return;
    }

    const formData = new FormData();
    formData.append('name', this.recipeForm.get('name')?.value || '');
    formData.append('type', this.recipeForm.get('type')?.value || '');
    formData.append('instructions', this.recipeForm.get('instructions')?.value || '');
    formData.append('image', this.selectedFile);
    formData.append('ingredients', JSON.stringify(this.recipeForm.get('ingredients')?.value));

    this.recipeService.addRecipe(formData).subscribe({
      next: () => {
        alert('המתכון נשמר בהצלחה! 🥗');
        this.recipeForm.reset({ type: 'Dairy' });
        this.ingredients.clear();
        this.ingredients.push(this.createIngredientGroup());
        this.selectedFile = null;
      },
      error: (err) => {
        const serverError = err.error?.error || 'שגיאה לא ידועה';
        alert('שגיאה בשמירה מהשרת: ' + JSON.stringify(serverError));
      }
    });
  }
}