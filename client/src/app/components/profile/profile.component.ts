// בס"ד - profile.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../auth.service';
import { RecipeService } from '../../recipe.service';
import { AddRecipeComponent } from '../add-recipe/add-recipe.component';
import { User } from '../../models/user.model';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, AddRecipeComponent],
  templateUrl: './profile.component.html'
})
export class ProfileComponent implements OnInit {
  user: User | null = null;
  requests: any[] = [];
  allUsers: any[] = [];
  archivedRecipes: any[] = [];
  showAddForm: boolean = false;

  constructor(public auth: AuthService, private recipeService: RecipeService) {
    this.user = this.auth.getUser();
  }

  ngOnInit() {
    if (this.user?.id) {
      this.auth.refreshStatus(this.user.id).subscribe({
        next: (res: Partial<User>) => {
          this.user = { ...this.user!, ...res };
          if (this.user.role === 'Admin') {
            this.loadRequests();
            this.loadAllUsers();
            this.loadArchivedRecipes();
          }
        }
      });
    }
  }

  requestUpgrade() {
    this.auth.sendUpgradeRequest(this.user!.id).subscribe(() => {
      alert('בקשת השדרוג נשלחה בהצלחה! המתן לאישור מנהל.');
      this.user!.has_requested = true;
    });
  }

  loadArchivedRecipes() {
    this.recipeService.getArchivedRecipes().subscribe(res => this.archivedRecipes = res);
  }

  restoreRecipe(id: number) {
    if (confirm('האם לשחזר מתכון זה מהארכיון?')) {
      this.recipeService.restoreRecipe(id).subscribe(() => {
        alert('המתכון שוחזר!');
        this.loadArchivedRecipes();
      });
    }
  }

  loadRequests() { this.auth.getAdminRequests().subscribe(res => this.requests = res); }
  loadAllUsers() { this.auth.getAllUsers().subscribe(res => this.allUsers = res); }
  approve(userId: number) { this.auth.approveUser(userId).subscribe(() => { this.loadRequests(); this.loadAllUsers(); }); }
}