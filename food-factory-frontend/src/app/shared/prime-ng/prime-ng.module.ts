import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';       
import { DropdownModule } from 'primeng/dropdown';   
import { PasswordModule } from 'primeng/password'; 
import { MultiSelectModule } from 'primeng/multiselect';
import { InputMaskModule } from 'primeng/inputmask';
import { ToastModule } from 'primeng/toast';
import { PanelModule } from 'primeng/panel';
import { CardModule } from 'primeng/card';
import { TableModule } from 'primeng/table';
import { ChartModule } from 'primeng/chart';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { FileUploadModule } from 'primeng/fileupload';
import { DialogModule } from 'primeng/dialog';
import { MessageModule } from 'primeng/message';
import { CalendarModule } from 'primeng/calendar';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

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
        ToastModule,
        PanelModule,
        CardModule,
        TableModule,
        ChartModule,
        TieredMenuModule,
        FileUploadModule,
        DialogModule,
        MessageModule,
        CalendarModule,
        ProgressSpinnerModule
    ]
})

export class PrimeNgModule{}