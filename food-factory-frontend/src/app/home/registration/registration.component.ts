import { Component } from '@angular/core';
import { RegistrationForm, RequestResponse } from '../../shared/interface/user';
import { USER_ROLE } from '../../shared/interface/multiselectFormat';
import { createFormData } from '../../shared/utils/utils';
import { UsersService } from '../../shared/services/users.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent {
  constructor(
    private userService: UsersService,
    private router: Router
  ) { }

  username: string = '';
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  roleOptions = USER_ROLE;
  role: { name: string } = { name: '' };
  isLoading: Boolean = false;

  onSubmit() {
    if (this.password !== this.confirmPassword) {
      alert("Passwords do not match!");
      return;
    } else {
      this.isLoading = true;
      console.log('Loading started');
      const formData = createFormData(this.username, this.email, this.password, this.role);
      this.userService.insertUser(formData).subscribe(
        res => {
          this.resetForm();
          this.router.navigate(['/login']);
        },
        error => {
          console.error('Error during registration:', error);
          this.isLoading = false;
        }
      );
      setTimeout(() => {
        this.isLoading = false;
      }, 6000);
    }
  }

  resetForm() {
    this.username = '';
    this.email = '';
    this.password = '';
    this.confirmPassword = '';
    this.role = { name: '' };
  }

  isFormEmpty(): boolean {
    return !this.username && !this.email && !this.password && !this.confirmPassword && !this.role;
  }
}
