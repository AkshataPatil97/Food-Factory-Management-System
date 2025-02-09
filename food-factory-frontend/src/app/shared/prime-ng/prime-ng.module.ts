import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';       
import { DropdownModule } from 'primeng/dropdown';   
import { PasswordModule } from 'primeng/password'; 
import { MultiSelectModule } from 'primeng/multiselect';
import { InputMaskModule } from 'primeng/inputmask';
import { ToastModule } from 'primeng/toast';

@NgModule({
    declarations:[],
    imports: [
        CommonModule
    ],
    exports: [
        ButtonModule,
        InputTextModule,
        DropdownModule,
        PasswordModule,
        MultiSelectModule,
        InputMaskModule,
        ToastModule
    ]
})

export class PrimeNgModule{}