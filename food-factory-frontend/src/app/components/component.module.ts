import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserRegistrationComponent } from './user-registration/user-registration.component';
import { PrimeNgModule } from '../shared/prime-ng/prime-ng.module';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';



@NgModule({
  declarations: [UserRegistrationComponent],
  imports: [
    CommonModule,
    PrimeNgModule,
    HttpClientModule,
    FormsModule
  ]
})
export class ComponentModule { }
