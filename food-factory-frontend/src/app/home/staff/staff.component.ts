import { Component, OnInit, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { UsersService } from '../../shared/services/users.service';
import { jwtDecode } from 'jwt-decode';
import { OrdersService } from '../../shared/services/orders.service';
import { MessageService } from 'primeng/api';
import { trigger, style, animate, transition } from '@angular/animations';
import { LoaderService } from '../../shared/services/loader.service';

interface UserDetails {
  userId: number | null;
  userName: string;
  phone: string;
  staffType: string;
  orderId: number | null;
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
  email: string;
  username: string;
  role: string;
  id: number;
  user_id: number;
  shop_name: string | null;
  address_payload: string | null;
  created_at: string;
  updated_at: string;
  is_deleted: boolean;
  mobile_no: string | null;
  profile_photo: string | null;
  about: string | null;
  is_active: boolean;
}

export interface Order {
  order_id: number;
  user_id: number;
  user: User;
  total_price: number;
  status: string;
  order_date: string;
  updated_at: string;
  is_cancelled: boolean;
  cancellation_reason: string | null;
  order_items: OrderItem[];
}

@Component({
  selector: 'app-staff',
  templateUrl: './staff.component.html',
  styleUrls: ['./staff.component.scss'],
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'scale(0.5)' }),
        animate('300ms ease-out', style({ opacity: 1, transform: 'scale(1)' }))
      ])
    ])
  ]
})
export class StaffComponent implements OnInit {
  phoneNumber = '';
  loading = false;
  errorMessage = '';
  isLoggedIn = false;
  staffRole = '';
  userDetails: UserDetails = this.getDefaultUserDetails();
  assignedDeliveries: Order | null = null;
  userId: number | null = null;
  orderId: number | null = null;
  email = '';
  otpCode = '';
  orderDialog: any = {};
  showDetailDialog = false;
  showOtpDialog = false;
  pendingOrders: any[] = [];
  processingOrders: any[] = [];
  allOrders: any[] = [];
  showPendingOrders = false;
  showProcessingOrders = false;

  constructor(
    private userService: UsersService,
    private orderService: OrdersService,
    private messageService: MessageService,
    private cdr: ChangeDetectorRef,
    private loadingService: LoaderService
  ) { }

  ngOnInit() {
    const token = localStorage.getItem('staffToken');
    const role = localStorage.getItem('staffRole');

    if (token && role) {
      this.isLoggedIn = true;
      this.staffRole = role;
      this.extractUserIdFromToken(token);
      if (this.staffRole === 'Delivery' && this.userId) {
        this.fetchAssignedDeliveries();
      }
      this.fetchAllOrders();
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    this.refresh();
  }

  refresh() {
    if (this.staffRole === 'Delivery' && this.userId) {
      this.fetchAssignedDeliveries();
    }
    this.fetchAllOrders();
  }

  onSubmit() {
    if (this.isInvalidPhoneNumber) {
      this.errorMessage = 'Enter a valid 10-digit phone number.';
      return;
    }

    this.loadingService.show();
    this.userService.staffLogin(this.phoneNumber).subscribe({
      next: (res: any) => {
        localStorage.setItem('staffToken', res.token);
        localStorage.setItem('staffPhone', res.phone);
        localStorage.setItem('staffRole', res.role);
        this.isLoggedIn = true;
        this.staffRole = res.role;
        this.extractUserIdFromToken(res.token);
        this.fetchAllOrders();

        if (this.staffRole === 'Delivery Boy' && this.userId) {
          this.fetchAssignedDeliveries();
        }

        this.loadingService.hide();
      },
      error: (err: any) => {
        this.errorMessage = err.error.error || 'Login failed';
        this.loadingService.hide();
      }
    });
  }

  extractUserIdFromToken(token: string) {
    try {
      const decoded: any = jwtDecode(token);
      this.userDetails = {
        userId: decoded.user_id,
        userName: decoded.user_name,
        phone: decoded.phone,
        staffType: decoded.role,
        orderId: decoded.order_id,
      };
      this.userId = decoded.user_id;
      this.orderId = decoded.order_id;
      this.staffRole = decoded.role;
    } catch (error) {
      console.error('Invalid token:', error);
    }
  }

  fetchAssignedDeliveries() {
    if (!this.userId) return;
    this.orderService.getAssignedDelivery(this.orderId).subscribe({
      next: (res: any) => {
        this.assignedDeliveries = res.data?.status === 'Shipped' ? res.data : null;
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        console.error('Error fetching deliveries:', err);
      }
    });
  }

  fetchAllOrders() {
    this.loadingService.show();
    this.orderService.fetchAllOrderForAdmin().subscribe({
      next: (res: any) => {
        this.allOrders = res.data;
        this.pendingOrders = this.allOrders.filter(order => order.status === 'Pending');
        this.processingOrders = this.allOrders.filter(order => order.status === 'Processing');
        this.cdr.detectChanges();
        this.loadingService.hide();
      },
      error: (err: any) => {
        console.error('Error fetching orders:', err);
      }
    });
  }

  logout() {
    ['staffToken', 'staffRole', 'staffPhone'].forEach(item => localStorage.removeItem(item));
    this.resetState();
    this.showMessage('success', 'Success', 'Logged out successfully.');
  }

  openOrderDialog(order: any) {
    this.orderDialog = order;
    this.showDetailDialog = true;
  }

  openOtpDialog(orderId: number, email: string) {
    this.showDetailDialog = false;
    this.loadingService.show();
    this.userService.staffSendOTP(email).subscribe({
      next: () => {
        this.showOtpDialog = true;
        this.loadingService.hide();
        this.showMessage('success', 'Success', 'OTP sent to your email.');
      }
    });
    this.orderId = orderId;
    this.email = email;
  }

  verifyOtp(email: string) {
    this.loadingService.show();
    const status = 'Delivered';
    this.userService.staffVerifyOTP(email, this.otpCode, this.orderId, status, this.userId).subscribe({
      next: () => {
        this.showMessage('success', 'Success', 'OTP Verified.');
        this.showMessage('success', 'Success', 'Order Delivered!!!.');
        this.showOtpDialog = false;
        this.loadingService.hide();
        this.refresh();
      },
      error: () => {
        this.showMessage('error', 'Error', 'OTP verification failed.');
        this.showOtpDialog = false;
        this.loadingService.hide();
      }
    });
  }

  get formattedAddress(): string {
    try {
      const address = this.assignedDeliveries?.user.address_payload;
      return address ? this.getFormattedAddress(JSON.parse(address)) : 'Address not available';
    } catch {
      return 'Invalid address data';
    }
  }

  getFormattedAddress(addr: any): string {
    const { street, landmark, city, state, zip } = addr || {};
    return [street, landmark, city, state].filter(Boolean).join(', ') + (zip ? ` - ${zip}` : '');
  }

  get isInvalidPhoneNumber(): boolean {
    return !/^\d{10}$/.test(this.phoneNumber);
  }

  showPendingOrdersDialog() {
    this.showPendingOrders = true;
  }

  showProcessingOrdersDialog() {
    this.showProcessingOrders = true;
  }

  updateStatus(order: any, status: string) {
    const staff_id = this.userId ?? 0;
    this.loadingService.show();
    this.orderService.updateOrderStatus(order.order_id, status, staff_id).subscribe({
      next: () => {
        this.showMessage('success', 'Success', `Order moved to ${status} state.`);
        // Fetch the updated orders and deliveries again
        this.fetchAllOrders();
        if (this.staffRole === 'Delivery' && this.userId) {
          this.fetchAssignedDeliveries();
        }
        this.loadingService.hide();
      },
      error: (err) => {
        this.showMessage('error', 'Error', 'Failed to update order status.');
        console.error('Error updating order status:', err);
        this.loading = false;
        this.loadingService.hide();
      }
    });
  }


  private getDefaultUserDetails(): UserDetails {
    return {
      userId: null,
      userName: '',
      phone: '',
      staffType: '',
      orderId: null
    };
  }

  private resetState() {
    this.isLoggedIn = false;
    this.staffRole = '';
    this.phoneNumber = '';
    this.userId = null;
    this.orderId = null;
    this.userDetails = this.getDefaultUserDetails();
    this.pendingOrders = [];
    this.processingOrders = [];
    this.allOrders = [];
  }

  private showMessage(severity: string, summary: string, detail: string) {
    this.messageService.add({ severity, summary, detail });
  }
}
