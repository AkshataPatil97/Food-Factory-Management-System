import { NgModule } from "@angular/core";
import { HomeComponent } from "./home.component";
import { CommonModule } from "@angular/common";
import { CommonsModule } from "../commons/commons.module";
import { HomeRoutingModule } from "./home-routing.module";
import { PrimeNgModule } from "../shared/prime-ng/prime-ng.module";
import { RegistrationComponent } from "./registration/registration.component";
import { FormsModule } from "@angular/forms";
import { LoginComponent } from "./login/login.component";
import { AdminDashboardComponent } from "./admin-dashboard/admin-dashboard.component";
import { CustomerDashboardComponent } from "./customer-dashboard/customer-dashboard.component";
import { ProductComponent } from "./product/product.component";

@NgModule({
    declarations: [
        HomeComponent,
        RegistrationComponent,
        LoginComponent,
        AdminDashboardComponent,
        CustomerDashboardComponent,
        ProductComponent
    ],
    imports: [
        CommonModule,
        CommonsModule,
        HomeRoutingModule,
        PrimeNgModule,
        FormsModule
    ],
    exports: [
        HomeComponent,
        RegistrationComponent,
        LoginComponent,
        AdminDashboardComponent,
        CustomerDashboardComponent
    ]
})
export class HomeModule { }