import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { HttpClientModule } from "@angular/common/http";
import { AppComponent } from "./app.component";
import { PrimeNgModule } from "./shared/prime-ng/prime-ng.module";
import { AppRoutingModule } from "./app-routing.module";
import { RouterModule } from "@angular/router"; 
import { CommonsModule } from "./commons/commons.module";
import { FormsModule } from "@angular/forms";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    HttpClientModule,
    PrimeNgModule,
    AppRoutingModule, 
    RouterModule,
    FormsModule,
    CommonsModule
  ],
  exports: [RouterModule, CommonsModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
