import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { DbConfigService } from '../../shared/services/db-config.service';
import { ALLOW_ADMIN_REGISTER } from '../../shared/constants';
import { MessageService } from 'primeng/api';
import { AuthService } from '../../shared/services/auth.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent {
  allowAdminRegistration = false;
  allowAdminValue: string = '';
  userRole: string = '';

  constructor(
    private http: HttpClient,
    private dbService: DbConfigService,
    private messageService: MessageService,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    this.setUserRole()
  }

  setUserRole(){
    const user = this.authService.getUser(); 
    if (user && user.user_name) {
      this.userRole = user.role;
      // this.fetchAllDetails(this.userRole)
    } else {
      this.userRole = 'Guest';
    }
  }

  // fetchAllDetails(user) {

  // }

  updateAllowAdminRegisterSettings() {
    this.dbService.fetchDBConfig(ALLOW_ADMIN_REGISTER).subscribe(res => {
      this.allowAdminValue = res.db_config;
      const newValue = this.allowAdminValue === 'true' ? 'false' : 'true';
      this.updateValueInDbConfig(newValue);
    });
  }
  
  updateValueInDbConfig(dbVal: string) {
    if (dbVal === 'true'){
      this.showMessage('warn','Warn','Allow Admin Registration Enabled!!!')
    } else{
      this.showMessage('success','Success','Allow Admin Registration Disabled')
    }
    this.dbService.updateDBConfig(ALLOW_ADMIN_REGISTER, dbVal).subscribe(res => {
      console.log("DB Config updated:", res);
    });
  }

  showMessage(strSeverity: string,strSummary: string,strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }
  
}

