import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';

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
    private router: Router,
    private messageService: MessageService
  ) { }

  get isInvalidEmail(): boolean {
    return typeof this.email === 'string' && !/@/.test(this.email);
  }
  onSubmit() {
    this.authService.loginWithEmailAndPassword(this.email, this.password).subscribe(
      (response: any) => {
        if (response.token) {
          this.authService.storeToken(response.token); 

          const user = this.authService.getUser();  
          if (user?.role === 'Admin') {
            this.router.navigate(['/admin-dashboard']);
          } else if (user?.role === 'Dealer') {
            this.router.navigate(['/dealer-dashboard']);
          } else {
            this.showMessage('warn','Warn','Unknown user role. Please contact support.')
          }
        }
      },
      (error) => {
        if (error.error && error.error.error) {
          this.showMessage('error','Error',error.error.error)
        } else {
          this.showMessage('error','Error','Something went wrong. Please try again.')
        }
      }
    );
  }

  isFormFilled(): boolean {
    return this.email.trim() !== '' || this.password.trim() !== '';
  }  

  navigateToSignUp(){
    this.router.navigate(['/registration'])
  }

  showMessage(strSeverity: string,strSummary: string,strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }
}
