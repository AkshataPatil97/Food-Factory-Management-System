import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HeaderComponent } from "./header/header.component";
import { FooterComponent } from "./footer/footer.component";
import { WaveLoaderComponent } from "./wave-loader/wave-loader.component";

@NgModule({
    declarations: [
        HeaderComponent,
        FooterComponent,
        WaveLoaderComponent
    ],
    imports: [
        CommonModule
    ],
    exports: [
        HeaderComponent,
        FooterComponent,
        WaveLoaderComponent
    ]
})
export class CommonsModule { }