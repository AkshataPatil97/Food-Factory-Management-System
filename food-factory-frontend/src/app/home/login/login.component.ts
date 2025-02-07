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
  ) {}

  onSubmit() {
    this.authService.loginWithEmailAndPassword(this.email, this.password).subscribe(
      (response: any) => {
        this.authService.storeToken(response.token);
        console.log('Logged in');
        
        // this.router.navigate(['/dashboard']);
      },
      (error) => {
        console.error('Login failed!', error);
      }
    );
  }
}
