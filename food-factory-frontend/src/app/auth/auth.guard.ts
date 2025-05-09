import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../shared/services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private authService: AuthService, private router: Router) {}

  canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    const user = this.authService.getUser();  // ✅ Get user details from JWT token
    
    if (this.authService.isAuthenticated()) {
      if (next.routeConfig?.path === 'admin-dashboard' && user?.role !== 'Admin') {
        this.router.navigate(['/dealer-dashboard']);
        return false;
      }
      if (next.routeConfig?.path === 'dealer-dashboard' && user?.role !== 'Dealer') {
        this.router.navigate(['/admin-dashboard']);
        return false;
      }
      return true;
    } else {
      this.router.navigate(['/login']);
      return false;
    }
  }
}
