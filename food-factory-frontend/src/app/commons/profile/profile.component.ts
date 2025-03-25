import { Component } from '@angular/core';
import { MessageService } from 'primeng/api';
import { AuthService } from '../../shared/services/auth.service';
import { UsersService } from '../../shared/services/users.service';
import { HttpEvent } from '@angular/common/http';
import { Dealer } from '../../shared/interface/user';
import { UploadEvent } from 'primeng/fileupload';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent {
  userId: number = 0;
  updatedData: string | number = '';
  dealer: Dealer = {} as Dealer;
  updateFieldName: string = '';
  updateInputType: string = 'text';
  showFieldUpdateForm: boolean = false;
  showAddressUpdateForm: boolean = false;
  addressString: string = '';
  userRole: string = '';
  street: string = '';
  landmark: string = '';
  city: string = '';
  state: string = '';
  zip: number = 0;

  constructor(
    private messageService: MessageService,
    private authService: AuthService,
    private userService: UsersService
  ) { }

  ngOnInit(): void {
    this.setUserId();
    if (this.userId) {
      this.userService.fetchDealerData(this.userId, this.userRole).subscribe({
        next: (response) => {
          if (response) {
            console.log("Dealer Details fetched!!");

            let addressData = response.dealer_details.address_payload
              ? JSON.parse(response.dealer_details.address_payload)
              : {};

            // Handle profile photo: Use Base64 or a default image
            let profilePhoto = response.dealer_details.profile_photo
              ? `data:image/png;base64,${response.dealer_details.profile_photo}`
              : 'assets/images/Profile.jpg'; // Default image

            this.dealer = {
              address_payload: this.getFormattedAddress(addressData),
              created_at: response.dealer_details.created_at ? new Date(response.dealer_details.created_at) : new Date(),
              id: response.dealer_details.id || null,
              is_deleted: response.dealer_details.is_deleted || false,
              mobile_no: response.dealer_details.mobile_no || null,
              profile_photo: profilePhoto, // Store Base64 image or default
              shop_name: response.dealer_details.shop_name || '',
              updated_at: response.dealer_details.updated_at ? new Date(response.dealer_details.updated_at) : new Date(),
              user_id: response.dealer_details.user_id || null,
              email: response.dealer_details.email || '',
              user_name: response.dealer_details.username || '',
              about: response.dealer_details.about || ''
            };
          }
        },
        error: (error) => {
          console.error("Error fetching dealer details:", error);
        }
      });
    }
  }

  setUserId() {
    const user = this.authService.getUser();
    if (user && user.user_id) {
      this.userId = user.user_id;
      this.userRole = user.role;
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.dealer.profile_photo = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  saveProfile() {
    alert('Profile Saved Successfully!');
  }

  onSubmit() {
    this.userService.updateDealerDetails(this.updateFieldName, this.updatedData, this.userId).subscribe({
      next: (response) => {
        this.showMessage('success', 'Success', response.message);
        this.updatedData = '';
        this.showFieldUpdateForm = false;
        this.ngOnInit();
      },
      error: (error) => {
        this.showMessage('error', 'Error', 'Error in updating dealer details');
        console.error("Error in updating dealer details:", error);
      }
    });
  }

  cancelOperation() {
    this.showFieldUpdateForm = false;
    this.updatedData = '';
    this.showAddressUpdateForm = false;
  }

  addDetails(updatingField: string) {
    this.showFieldUpdateForm = true;
    if (updatingField === 'Mobile Number') {
      this.updateFieldName = updatingField;
      this.updateInputType = 'number';
    } else if (updatingField === 'Business Name' || updatingField === 'Address' || updatingField === 'Name' || updatingField === 'Email' || updatingField === 'About') {
      this.updateFieldName = updatingField;
      this.updateInputType = 'text';
    } else if (updatingField === 'Profile Photo') {
      this.updateFieldName = updatingField;
    }
  }

  showMessage(strSeverity: string, strSummary: string, strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }

  isFormEmpty(): boolean {
    return !this.street && !this.landmark && !this.city && !this.state && !this.zip;
  }
  addAddress() {
    this.showAddressUpdateForm = true;
  }
  onAddressSubmit() {
    const addressPayload = {
      street: this.street,
      landmark: this.landmark,
      city: this.city,
      state: this.state,
      zip: this.zip
    };

    // Convert the payload to a string
    this.addressString = JSON.stringify(addressPayload);
    this.userService.updateDealerDetails("Address", this.addressString, this.userId).subscribe({
      next: (response) => {
        this.showMessage('success', 'Success', response.message);
        this.updatedData = '';
        this.showFieldUpdateForm = false;
        this.ngOnInit();
      },
      error: (error) => {
        this.showMessage('error', 'Error', 'Error in updating dealer details');
        console.error("Error in updating dealer details:", error);
      }
    });
    this.showAddressUpdateForm = false;
  }

  getFormattedAddress(address: any): string {
    if (address && Object.keys(address).length > 0) { 
      const { street, landmark, city, state, zip } = address;
      return `${street}, ${landmark}, ${city}, ${state} - ${zip}`;
    }
    return '';
  }
  

  onUpload(event: any) {
    const file = event.files[0];
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64Image = reader.result as string;
        this.uploadImageToBackend(base64Image);
      };
      reader.onerror = error => console.error("Error converting file to Base64:", error);
    }
  }

  uploadImageToBackend(base64Image: string) {
    const payload = {
      profile_photo: base64Image.split(',')[1]
    };

    console.log(payload);
    this.userService.updateDealerDetails(this.updateFieldName, payload.profile_photo, this.userId).subscribe({
      next: (response) => {
        this.showMessage('success', 'Success', response.message);
        this.updatedData = '';
        this.showFieldUpdateForm = false;
        this.ngOnInit();
      },
      error: (error) => {
        this.showMessage('error', 'Error', 'Error in updating dealer details');
        console.error("Error in updating dealer details:", error);
      }
    });
  }

}


