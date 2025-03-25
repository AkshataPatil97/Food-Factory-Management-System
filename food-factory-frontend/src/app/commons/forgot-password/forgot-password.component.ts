import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UsersService } from '../../shared/services/users.service';
import { MessageService } from 'primeng/api';

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
    private userService: UsersService,
    private messageService: MessageService
  ) { }

  sendOTP() {
    this.isLoading = true;
    this.userService.verifyEmailSendOtp(this.email).subscribe({
      next: (res) => {
        this.step = 2;
        this.showMessage('success', 'Success', 'OTP sent successfully.');
      },
      error: (error) => {
        this.showMessage('error', 'Error', `Error while sending OTP: ${error.message || error}`);
        this.isLoading = false;
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }  

  verifyOTP() {
    this.isLoading = true;
    this.userService.verifyOTP(this.email, this.otp).subscribe(
      (res: any) => {
        if (res.success) {
          this.step = 3
          this.showMessage('success', 'Success', 'OTP verified successfully.')
        } else {
          this.showMessage('error', 'Error', `OTP verification failed: ${res.message || res}`)
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
          this.showMessage('success','Success','New password set!')
          this.router.navigate(['/login']);
        } else {
          this.showMessage('error', 'Error', `Reset password failed: ${res.message || res}`)
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

  showMessage(strSeverity: string, strSummary: string, strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }
}
