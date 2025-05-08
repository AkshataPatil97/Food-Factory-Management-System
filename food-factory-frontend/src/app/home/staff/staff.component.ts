import { Component, OnInit, SimpleChanges } from '@angular/core';
import { UsersService } from '../../shared/services/users.service';
import { jwtDecode } from 'jwt-decode';
import { OrdersService } from '../../shared/services/orders.service';
import { MessageService } from 'primeng/api';

interface UserDetails {
  userId: number | null;           // User ID can be a number or null
  userName: string;                // User name should be a string
  phone: string;                   // Alternate phone should be a string
  staffType: string;               // Staff type should be a string
  orderId: number | null;          // Order ID can be a number or null
}

export interface OrderItem {
  order_item_id: number;
  product_id: string;
  product_name: string;
  quantity: number;
  price_at_order: number;
  sub_total: number;
}

export interface User {
  email: string;                   // User's email address
  username: string;                // User's username (Name)
  role: string;                    // User's role (Dealer, Admin, etc.)
  id: number;                      // Unique identifier for the user
  user_id: number;                 // Linking field to the user ID (used for relationships)
  shop_name: string | null;        // Name of the shop (if applicable)
  address_payload: string | null;  // Address details in JSON format (if applicable)
  created_at: string;              // Record creation timestamp
  updated_at: string;              // Record last updated timestamp
  is_deleted: boolean;             // Soft delete flag (1: deleted, 0: active)
  mobile_no: string | null;        // Contact number of the user
  profile_photo: string | null;    // Profile photo URL (optional)
  about: string | null;            // Additional information about the user (optional)
  is_active: boolean;              // Indicates if the user is currently active (1: active, 0: inactive)
}

export interface Order {
  order_id: number;
  user_id: number;
  user: User;
  total_price: number;
  status: string;
  order_date: string; // Consider using Date type if you plan to parse it
  updated_at: string; // Same here, use Date if needed
  is_cancelled: boolean;
  cancellation_reason: string | null;
  order_items: OrderItem[];
}


@Component({
  selector: 'app-staff',
  templateUrl: './staff.component.html',
  styleUrls: ['./staff.component.scss']
})
export class StaffComponent implements OnInit {
  phoneNumber: string = '';
  loading = false;
  errorMessage: string = '';
  isLoggedIn = false;
  userDetails: UserDetails = {
    userId: null,
    userName: '',
    phone: '',
    staffType: '',
    orderId: null
  };
  staffRole = '';
  assignedDeliveries: Order | null = null;
  userId: number | null = null;
  orderId: number | null = null;
  email: string = '';
  otpCode: string = '';

  constructor(
    private userService: UsersService,
    private orderService: OrdersService,
    private messageService: MessageService
  ) { }

  ngOnInit() {
    // Check if staff is already logged in
    const token = localStorage.getItem('staffToken');
    const staffRole = localStorage.getItem('staffRole');

    if (token && staffRole) {
      this.isLoggedIn = true;
      this.staffRole = staffRole;
      this.extractUserIdFromToken(token);
      console.log(localStorage);

      if (this.staffRole === 'Delivery' && this.userId) {
        this.fetchAssignedDeliveries();
      }
    }
    this.refresh();
  }

  ngOnChanges(changes: SimpleChanges) {
    this.refresh();
  }

  refresh() {
    this.fetchAssignedDeliveries();
  }

  onSubmit() {
    if (!this.phoneNumber.match(/^\d{10}$/)) {
      this.errorMessage = 'Enter a valid 10-digit phone number.';
      return;
    }

    this.loading = true;

    this.userService.staffLogin(this.phoneNumber).subscribe({
      next: (res: any) => {
        console.log(res);

        // Store necessary details in localStorage
        localStorage.setItem('staffToken', res.token);
        localStorage.setItem('staffPhone', res.phone);
        localStorage.setItem('staffRole', res.role);  // Store staff role
        this.isLoggedIn = true;

        // Extract user details and store them in the component's state
        this.extractUserIdFromToken(res.token); // Extract user_id

        if (this.staffRole === 'Delivery Boy' && this.userId) {
          this.fetchAssignedDeliveries();
        }
      },
      error: (err: any) => {
        this.errorMessage = err.error.error || 'Login failed';
        this.loading = false;
      }
    });
  }

  extractUserIdFromToken(token: string) {
    try {
      const decodedToken: any = jwtDecode(token);
      console.log(decodedToken);

      // Store the decoded token data into userDetails
      this.userDetails = {
        userId: decodedToken.user_id,
        userName: decodedToken.user_name,
        phone: decodedToken.phone,
        staffType: decodedToken.role,
        orderId: decodedToken.order_id,
      };
      console.log(this.userDetails);

      this.userId = decodedToken.user_id;
      this.orderId = decodedToken.order_id;

      // Update staffRole in case it is not set earlier
      this.staffRole = this.userDetails.staffType;
    } catch (error) {
      console.error('Error decoding token:', error);
    }
  }

  fetchAssignedDeliveries() {
    if (!this.userId) return;

    this.orderService.getAssignedDelivery(this.orderId).subscribe({
      next: (res: any) => {
        if (res.data && res.data.status === 'Shipped') {
          this.assignedDeliveries = res.data;
          console.log("Assigned Deliveries:", this.assignedDeliveries);
        } else {
          console.log("Order status is not 'Shipped'. No delivery assigned.");
          this.assignedDeliveries = null;
        }
      },
      error: (err: any) => {
        console.error('Error fetching deliveries:', err);
      }
    });
  }


  logout() {
    // Clear stored data from localStorage
    localStorage.removeItem('staffToken');
    localStorage.removeItem('staffRole');
    localStorage.removeItem('staffPhone');  // Optionally clear phone data

    // Reset the component state
    this.isLoggedIn = false;
    this.staffRole = '';
    this.phoneNumber = '';
    this.userId = null;
    this.orderId = null;
    this.userDetails = {
      userId: null,
      userName: '',
      phone: '',
      staffType: '',
      orderId: null
    };
    this.showMessage('success', 'Success', 'Logged out successfully.');
  }
  orderDialog: any = {}
  showDetailDialog: boolean = false;
  openOrderDialog(order: any) {
    this.orderDialog = order;
    this.showDetailDialog = true
  }

  showOtpDialog: boolean = false;

  // This will open the OTP dialog and pass the orderId
  openOtpDialog(orderId: number, email: string) {
    this.showDetailDialog = false;

    console.log(email);
    this.userService.staffSendOTP(email).subscribe({
      next: (res) => {
        this.showOtpDialog = true;
        this.showMessage('success', 'Success', 'OTP sent to your email.');
      }
    })
    this.orderId = orderId;
    this.email = email;
  }

  // This method will verify the OTP
  verifyOtp(email: string) {
    let status = 'Delivered'
    this.userService.staffVerifyOTP(email, this.otpCode, this.orderId, status, this.userId).subscribe({
      next: (res) => {
        this.showMessage('success', 'Success', 'OTP Verified.');
        this.showMessage('success', 'Success', 'Order Delivered!!!.');
        this.refresh();
      },
      error: (err) => {
        this.showMessage('error', 'Error', 'OTP verification failed.');
      }
    })
    this.showOtpDialog = false;
  }

  get formattedAddress(): string {
    if (this.assignedDeliveries?.user.address_payload) {
      const address = JSON.parse(this.assignedDeliveries.user.address_payload);
      return this.getFormattedAddress(address);
    }
    return 'Address not available';
  }
  getFormattedAddress(address: any): string {
    if (address && Object.keys(address).length > 0) {
      const { street, landmark, city, state, zip } = address;
      return `${street}, ${landmark}, ${city}, ${state} - ${zip}`;
    }
    return 'Address not available';
  }

  pendingOrders: any[] = []; // Orders with "Pending" status
  processingOrders: any[] = [];
  allOrders: any[] = [];
  showPendingOrders: boolean = false;
  showProcessingOrders: boolean = false;

  get isInvalidPhoneNumber(): boolean {
    return typeof this.phoneNumber === 'string' && !/^\d{10}$/.test(this.phoneNumber);
  }
  

  showPendingOrdersDialog() {
    this.orderService.fetchAllOrderForAdmin().subscribe({
      next: (res: any) => {
        this.allOrders = res.data; // Store all orders
        // Filter orders with status 'Pending'
        this.pendingOrders = this.allOrders.filter(order => order.status === 'Pending');
        this.showPendingOrders = true;
      },
      error: (err) => {
        console.error('Error fetching all orders:', err);
      }
    });
  }

  // To show the processing orders dialog
  showProcessingOrdersDialog() {
    this.orderService.fetchAllOrderForAdmin().subscribe({
      next: (res: any) => {
        this.allOrders = res.data; // Store all orders
        // Filter orders with status 'Processing'
        this.processingOrders = this.allOrders.filter(order => order.status === 'Processing');
        this.showProcessingOrders = true;
      },
      error: (err) => {
        console.error('Error fetching all orders:', err);
      }
    });
  }

  // Update order status
  updateStatus(order: any, status: string) {
    this.loading = true;
    let staff_id = 0;
    this.orderService.updateOrderStatus(order.order_id, status, staff_id).subscribe({
      next: () => {
        console.log(`Order ${order.order_id} updated to ${status}`);
        this.loading = false;
        if (status === 'Processing') {
          this.showMessage('success', 'Success', 'Order moved to Processing State.');
          this.showPendingOrdersDialog();
        } else {
          this.showMessage('success', 'Success', 'Order moved to Processed State.');
          this.showProcessingOrdersDialog();
        }
      },
      error: (err) => {
        console.error('Error updating order status:', err);
        this.loading = false;
      }
    });
  }

  // Refresh orders after status update
  refreshOrders() {
    this.showPendingOrders = false;
    this.showProcessingOrders = false;
    this.showPendingOrdersDialog();
    this.showProcessingOrdersDialog();
  }

  showMessage(strSeverity: string, strSummary: string, strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }

}
