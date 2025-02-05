import { NgModule } from "@angular/core";
import { HomeComponent } from "./home.component";
import { CommonModule } from "@angular/common";
import { CommonsModule } from "../commons/commons.module";
import { HomeRoutingModule } from "./home-routing.module";
import { FormsModule } from "@angular/forms";

@NgModule({
    declarations: [
        HomeComponent
    ],
    imports: [
        CommonModule,
        CommonsModule,
        HomeRoutingModule,
        FormsModule
    ],
    exports: [
        HomeComponent
    ]
})
export class HomeModule { }