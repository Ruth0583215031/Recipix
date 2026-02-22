export interface User {
  id: number;
  user_name: string;
  email: string;
  role: 'Reader' | 'Content' | 'Admin';
  is_approved: boolean;
  has_requested: boolean;
}