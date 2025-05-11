import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HeaderComponent } from "./header/header.component";
import { FooterComponent } from "./footer/footer.component";
import { WaveLoaderComponent } from "./wave-loader/wave-loader.component";
import { ForgotPasswordComponent } from "./forgot-password/forgot-password.component";
import { CommonsRoutingModule } from "./commons-routing.module";
import { PrimeNgModule } from "../shared/prime-ng/prime-ng.module";
import { FormsModule } from "@angular/forms";
import { SettingsComponent } from "./settings/settings.component";
import { ProfileComponent } from "./profile/profile.component";
import { LoaderComponent } from "./loader/loader.component";

@NgModule({
    declarations: [
        HeaderComponent,
        FooterComponent,
        WaveLoaderComponent,
        ForgotPasswordComponent,
        SettingsComponent,
        ProfileComponent,
        LoaderComponent
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
        ForgotPasswordComponent,
        SettingsComponent,
        ProfileComponent,
        LoaderComponent
    ]
})
export class CommonsModule { }