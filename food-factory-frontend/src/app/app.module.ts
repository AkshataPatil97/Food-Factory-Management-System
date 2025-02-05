import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { HttpClientModule } from "@angular/common/http";
import { AppComponent } from "./app.component";
import { PrimeNgModule } from "./shared/prime-ng/prime-ng.module";
import { AppRoutingModule } from "./app-routing.module";
import { RouterModule } from "@angular/router"; 
import { CommonsModule } from "./commons/commons.module";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    PrimeNgModule,
    AppRoutingModule, 
    RouterModule,
    CommonsModule
  ],
  exports: [RouterModule, CommonsModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
