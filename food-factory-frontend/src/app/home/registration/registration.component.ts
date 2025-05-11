import { Component, OnInit } from '@angular/core';
import { RegistrationForm } from '../../shared/interface/user';
import { USER_ROLE } from '../../shared/interface/multiselectFormat';
import { createFormData } from '../../shared/utils/utils';
import { UsersService } from '../../shared/services/users.service';
import { Router } from '@angular/router';
import { DbConfigService } from '../../shared/services/db-config.service';
import { ALLOW_ADMIN_REGISTER } from '../../shared/constants';
import { LoaderService } from '../../shared/services/loader.service';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {
  username = '';
  email = '';
  password = '';
  confirmPassword = '';
  roleOptions = [...USER_ROLE];
  role: { name: string } = { name: '' };

  constructor(
    private userService: UsersService,
    private router: Router,
    private dbService: DbConfigService,
    private loadingService: LoaderService
  ) {}

  ngOnInit(): void {
    this.dbService.fetchDBConfig(ALLOW_ADMIN_REGISTER).subscribe(response => {
      this.roleOptions.forEach(role => {
        if (role.name === 'Admin') {
          role.disabled = response.db_config === 'false';
        }
      });
    });
  }

  get isInvalidUsername(): boolean {
    return typeof this.username === 'string' && !/^[a-zA-Z ]+$/.test(this.username);
  }

  get isInvalidPassword(): boolean {
    return typeof this.password === 'string' && !/^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/.test(this.password);
  }

  // Check if email contains "@"
  get isInvalidEmail(): boolean {
    return typeof this.email === 'string' && !/@/.test(this.email);
  }
   

  onSubmit(): void {
    if (this.password !== this.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
    
    this.loadingService.show();
    const formData = createFormData(this.username, this.email, this.password, this.role);
    this.userService.insertUser(formData).subscribe({
      next: () => {
        this.resetForm();
        this.loadingService.hide();
        this.router.navigate(['/login']);
      },
      error: error => {
        console.error('Error during registration:', error);
      }
    });
    setTimeout(() => this.loadingService.hide(), 6000);
  }

  resetForm(): void {
    Object.assign(this, { username: '', email: '', password: '', confirmPassword: '', role: { name: '' } });
  }

  isFormEmpty(): boolean {
    return !this.username && !this.email && !this.password && !this.confirmPassword && !this.role.name;
  }

  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }
}
