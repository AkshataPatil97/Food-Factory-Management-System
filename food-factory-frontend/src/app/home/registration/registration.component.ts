import { Component, OnInit } from '@angular/core';
import { RegistrationForm } from '../../shared/interface/user';
import { USER_ROLE } from '../../shared/interface/multiselectFormat';
import { createFormData } from '../../shared/utils/utils';
import { UsersService } from '../../shared/services/users.service';
import { Router } from '@angular/router';
import { DbConfigService } from '../../shared/services/db-config.service';
import { ALLOW_ADMIN_REGISTER } from '../../shared/constants';

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
  isLoading = false;

  constructor(
    private userService: UsersService,
    private router: Router,
    private dbService: DbConfigService
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

  onSubmit(): void {
    if (this.password !== this.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
    
    this.isLoading = true;
    const formData = createFormData(this.username, this.email, this.password, this.role);
    this.userService.insertUser(formData).subscribe({
      next: () => {
        this.resetForm();
        this.router.navigate(['/login']);
      },
      error: error => {
        console.error('Error during registration:', error);
        this.isLoading = false;
      }
    });
    setTimeout(() => this.isLoading = false, 6000);
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
