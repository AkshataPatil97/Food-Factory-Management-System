import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';        
import { DropdownModule } from 'primeng/dropdown';    
import { FormsModule } from '@angular/forms';   

@NgModule({
    declarations:[],
    imports: [CommonModule],
    exports: [
        ButtonModule,
        InputTextModule,
        DropdownModule,
        FormsModule
    ]
})

export class PrimeNgModule{}