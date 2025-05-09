import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home.component';
import { RegistrationComponent } from './registration/registration.component'; 
import { LoginComponent } from './login/login.component';
import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
import { AuthGuard } from '../auth/auth.guard';
import { ForgotPasswordComponent } from '../commons/forgot-password/forgot-password.component';
import { StaffComponent } from './staff/staff.component';
import { DealerDashboardComponent } from './dealer-dashboard/dealer-dashboard.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'registration', component: RegistrationComponent }, 
  { path: 'login', component: LoginComponent },
  { path: 'admin-dashboard', component: AdminDashboardComponent, canActivate: [AuthGuard] },  
  { path: 'dealer-dashboard', component: DealerDashboardComponent, canActivate: [AuthGuard] },  
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'staff-login', component: StaffComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],  
  exports: [RouterModule]
})
export class HomeRoutingModule {}
