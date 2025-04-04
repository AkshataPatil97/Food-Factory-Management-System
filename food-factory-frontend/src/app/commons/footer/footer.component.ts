import { Component } from '@angular/core';
import { UsersService } from '../../shared/services/users.service';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {
  constructor( 
    private userService: UsersService
  ){}
  isFooterHidden: boolean = true;
  companyDetail: any = {};

  ngOnInit(): void {
    this.userService.fetchCompanyDetails().subscribe({
      next: (res)=>{
        this.companyDetail = res.data;
      }
    })
  }
  
  toggleFooter() {
    this.isFooterHidden = !this.isFooterHidden;
  }

}
