import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UsersService } from '../../shared/services/users.service';
import { MessageService } from 'primeng/api';
import { LoaderService } from '../../shared/services/loader.service';

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
    private messageService: MessageService,
    private loadingService: LoaderService
  ) { }

  sendOTP() {
    this.loadingService.show();
    this.userService.verifyEmailSendOtp(this.email).subscribe({
      next: (res) => {
        this.step = 2;
        this.showMessage('success', 'Success', 'OTP sent successfully.');
        this.loadingService.hide();
      },
      error: (error) => {
        this.showMessage('error', 'Error', `Error while sending OTP: ${error.message || error}`);
        this.loadingService.hide();
      },
      complete: () => {
        this.loadingService.hide();
      }
    });
  }  

  verifyOTP() {
    this.loadingService.show();
    this.userService.verifyOTP(this.email, this.otp).subscribe(
      (res: any) => {
        if (res.success) {
          this.step = 3
          this.showMessage('success', 'Success', 'OTP verified successfully.')
          this.loadingService.hide();
        } else {
          this.showMessage('error', 'Error', `OTP verification failed: ${res.message || res}`)
        }
      },
      (error) => {
        console.error("Error during OTP verification:", error);
        alert(error.error?.message || "An unexpected error occurred. Please try again.");
        this.loadingService.hide();
      }
    );
  }

  get isInvalidEmail(): boolean {
    return typeof this.email === 'string' && !/@/.test(this.email);
  }

  
  get isInvalidPassword(): boolean {
    return typeof this.password === 'string' && !/^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/.test(this.password);
  }

  get isInvalidOtp(): boolean {
    return typeof this.otp === 'string' && !/^\d{6}$/.test(this.otp);
  }
  
  resetPassword() {
    this.loadingService.show();
    this.userService.resetPassword(this.email, this.password).subscribe(
      (res: any) => {
        if (res.success) {
          this.showMessage('success','Success','New password set!')
          this.loadingService.hide();
          this.router.navigate(['/login']);
        } else {
          this.showMessage('error', 'Error', `Reset password failed: ${res.message || res}`)
        }
      },
      (error) => {
        console.error("Error during reset password:", error);
        alert(error.error?.message || "An unexpected error occurred. Please try again.");
        this.loadingService.hide();
      }
    );
  }

  showMessage(strSeverity: string, strSummary: string, strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }
}
