import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UsersService } from '../../shared/services/users.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent {

  email: string = '';
  otp: string = '';
  newPassword: string = '';
  step: number = 1; 
  isLoading: Boolean = false;

  constructor(
    private http: HttpClient, 
    private router: Router,
    private userService: UsersService
  ) { }

  sendOTP() {
    this.isLoading = true;
    this.userService.verifyEmailSendOtp(this.email).subscribe(
      res => {
        this.step = 2;
      },
      error => {
        console.error('Error during registration:', error);
        this.isLoading = false;
      }
    );
    setTimeout(() => {
      this.isLoading = false;  
    }, 3000);
  }

  verifyOTP() {
    this.http.post('/api/verify-otp/', { email: this.email, otp: this.otp }).subscribe(
      () => {
        alert('OTP Verified. Set a new password.');
        this.step = 3; // ✅ Move to password reset step
      },
      (error) => alert(error.error.error)
    );
  }

  resetPassword() {
    this.http.post('/api/reset-password/', { email: this.email, password: this.newPassword }).subscribe(
      () => {
        alert('Password reset successful. Please login.');
        this.router.navigate(['/login']);
      },
      (error) => alert(error.error.error)
    );
  }
}
