import { Component, Input } from '@angular/core';
import { UsersService } from '../../shared/services/users.service';
import { Dealer } from '../../shared/interface/user';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  @Input() userName: string='';
  @Input() userId: number=0;
  @Input() userRole: string='';

  dealerDetails: any;

  constructor(
    private userService : UsersService
  ) {}

  ngOnInit(): void {
    if (this.userId) {
      this.userService.fetchDealerData(this.userId, this.userRole).subscribe({
        next: (response) => {
          if (response) {
            console.log("Dealer Details fetched!!");

            // let addressData = response.dealer_details.address_payload
            //   ? JSON.parse(response.dealer_details.address_payload)
            //   : {};

            // Handle profile photo: Use Base64 or a default image
            let profilePhoto = response.dealer_details.profile_photo
              ? `data:image/png;base64,${response.dealer_details.profile_photo}`
              : 'assets/images/Profile.jpg'; // Default image

            this.dealerDetails = {
              // address_payload: this.getFormattedAddress(addressData),
              // created_at: response.dealer_details.created_at ? new Date(response.dealer_details.created_at) : new Date(),
              // id: response.dealer_details.id || null,
              // is_deleted: response.dealer_details.is_deleted || false,
              // mobile_no: response.dealer_details.mobile_no || null,
              profile_photo: profilePhoto, // Store Base64 image or default
              // shop_name: response.dealer_details.shop_name || '',
              // updated_at: response.dealer_details.updated_at ? new Date(response.dealer_details.updated_at) : new Date(),
              user_id: response.dealer_details.user_id || null,
              email: response.dealer_details.email || '',
              user_name: response.dealer_details.username || ''
            };
          }
        },
        error: (error) => {
          console.error("Error fetching dealer details:", error);
        }
      });
    }
  }
}
