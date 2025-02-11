import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  email: string = '';
  password: string = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  onSubmit() {
    this.authService.loginWithEmailAndPassword(this.email, this.password).subscribe(
      (response: any) => {
        if (response.token) {
          this.authService.storeToken(response.token); 

          const user = this.authService.getUser();  
          if (user?.role === 'Admin') {
            this.router.navigate(['/admin-dashboard']);
          } else if (user?.role === 'Customer') {
            this.router.navigate(['/customer-dashboard']);
          } else {
            alert("Unknown user role. Please contact support.");
          }
        }
      },
      (error) => {
        if (error.error && error.error.error) {
          alert(error.error.error);
        } else {
          alert("Something went wrong. Please try again.");
        }
      }
    );
  }
}
