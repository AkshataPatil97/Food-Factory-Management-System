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
  ){}

  username: string = '';
  email: string = '';
  password: string = '';
  roleOptions = USER_ROLE;
  role: { name: string } = { name: '' };

  onSubmit() {
    const formData = createFormData(this.username, this.email, this.password, this.role);
    this.userService.insertUser(formData).subscribe(
      res=> {
        this.resetForm();
        alert('Registered successfully! You will be redirected to the login page.');
        this.router.navigate(['/login']);
      }
    );
  }

  resetForm() {
    this.username = '';
    this.email = '';
    this.password = '';
    this.role = { name: '' };  
  }
}
