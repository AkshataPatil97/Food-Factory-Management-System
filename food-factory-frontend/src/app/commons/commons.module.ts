import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HeaderComponent } from "./header/header.component";
import { FooterComponent } from "./footer/footer.component";
import { WaveLoaderComponent } from "./wave-loader/wave-loader.component";
import { ForgotPasswordComponent } from "./forgot-password/forgot-password.component";
import { CommonsRoutingModule } from "./commons-routing.module";
import { PrimeNgModule } from "../shared/prime-ng/prime-ng.module";
import { FormsModule } from "@angular/forms";

@NgModule({
    declarations: [
        HeaderComponent,
        FooterComponent,
        WaveLoaderComponent,
        ForgotPasswordComponent
    ],
    imports: [
        CommonModule,
        CommonsRoutingModule,
        PrimeNgModule,
        FormsModule
    ],
    exports: [
        HeaderComponent,
        FooterComponent,
        WaveLoaderComponent,
        ForgotPasswordComponent
    ]
})
export class CommonsModule { }