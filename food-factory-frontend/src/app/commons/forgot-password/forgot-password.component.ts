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
  password: string = '';
  confirmPassword: string = '';
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
    this.isLoading = true;
    this.userService.verifyOTP(this.email, this.otp).subscribe(
      (res: any) => {
        if (res.success) {          
          this.step = 3;
        } else {
          console.error("OTP verification failed:", res.message);
          alert(res.message);
        }
      },
      (error) => {
        console.error("Error during OTP verification:", error);
        alert(error.error?.message || "An unexpected error occurred. Please try again.");
      }
    );
    setTimeout(() => {
      this.isLoading = false;
    }, 3000);
  }
  

  resetPassword() {
    this.isLoading = true;
    this.userService.resetPassword(this.email, this.password).subscribe(
      (res: any) => {
        if (res.success) {          
          this.router.navigate(['/login']);
        } else {
          console.error("Reset password failed:", res.message);
          alert(res.message);
        }
      },
      (error) => {
        console.error("Error during reset password:", error);
        alert(error.error?.message || "An unexpected error occurred. Please try again.");
      }
    );
    setTimeout(() => {
      this.isLoading = false;
    }, 3000);
  }
}
