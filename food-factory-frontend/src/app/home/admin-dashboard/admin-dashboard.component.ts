import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';
import { OrdersService } from '../../shared/services/orders.service';
import { CancelledOrder, Order } from '../../shared/interface/order';
import { MessageService } from 'primeng/api';
import { DeliveryboyService } from '../../shared/services/deliveryboy.service';
import { UsersService } from '../../shared/services/users.service';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { LoaderService } from '../../shared/services/loader.service';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.scss']
})
export class AdminDashboardComponent {
  chartData: any;
  activeComponent: string = 'dashboard';
  selectedProductAction: string = '';
  userName: string = '';
  userId: number = 0;
  userRole: string = '';
  currentOrders: Order[] = [];
  companyDetails: any = {};
  cancelledOrders: CancelledOrder[] = [];
  deliveredOrders: Order[] = [];

  constructor(
    private authService: AuthService,
    private orderService: OrdersService,
    private messageService: MessageService,
    private deliveryBoyService: DeliveryboyService,
    private userService: UsersService,
    private loadingService: LoaderService
  ) { }

  ngOnInit(): void {
    this.setUserId();
    this.refreshData();
    this.fetchInvoices()
    this.fetchComapnyDetails()
    setInterval(() => {
      this.refreshData();
    }, 300000); // Refresh every 5 minutes
  }

  refreshData() {
    this.fetchAllOrders();
    this.fetchAllCancelledOrders();
    this.fetchAllDeliveredOrders();
    this.checkDeliveryBoyAvailability();
    this.loadStaff();
    this.fetchInvoices();
  }

  onRefreshClick() {
    this.loadingService.show();

    this.refreshData();

    // Hide loader after 5 seconds
    setTimeout(() => {
      this.loadingService.hide();
    }, 5000);
  }


  logout() {
    this.authService.logout();
  }

  setUserId() {
    const user = this.authService.getUser();
    if (user && user.user_id) {
      this.userId = user.user_id;
      this.userRole = user.role;
      this.userName = user.user_name;
    }
  }

  setActiveComponent(component: string, productAction: string = '') {
    this.activeComponent = component;
    this.selectedProductAction = productAction;
  }

  // Check if the main component is active
  isActiveComponent(component: string): boolean {
    return this.activeComponent === component;
  }

  // Check if the sub-menu is active
  isSubActiveComponent(action: string): boolean {
    return this.activeComponent === 'product' && this.selectedProductAction === action;
  }

  fetchComapnyDetails() {
    this.userService.fetchCompanyDetails().subscribe({
      next: (res) => {
        this.companyDetails = res.data;
      }
    })
  }

  fetchAllOrders() {
    this.orderService.fetchAllOrderForAdmin().subscribe({
      next: (response) => {
        this.currentOrders = response.data.map((order: any) => ({
          orderId: order.order_id,
          date: order.order_date,
          totalPrice: order.total_price,
          status: order.status,
          order_items: order.order_items || [],
          user: order.user
        }));
      },
      error: (error) => {
        console.log(error);
      }
    });

  }


  fetchAllCancelledOrders() {
    this.orderService.fetchAllCancelledOrderForAdmin().subscribe({
      next: (response) => {
        this.cancelledOrders = response.data.map((order: any) => ({
          reason: order.cancellation_reason,
          date: order.order_date,
          totalPrice: order.total_price,
          status: order.status,
          order_items: order.order_items || [],
          user: order.user
        }));
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  fetchAllDeliveredOrders() {
    this.orderService.fetchAllDeliveredOrderForAdmin().subscribe({
      next: (response) => {
        this.deliveredOrders = response.data.map((order: any) => ({
          orderId: order.order_id,
          date: order.order_date,
          totalPrice: order.total_price,
          status: order.status,
          order_items: order.order_items || [],
          user: order.user
        }));
      },
      error: (error) => {
        console.log(error);
      }
    });
  }
  allInvoices: any = {};
  fetchInvoices() {
    this.orderService.fetchAllInvoices().subscribe({
      next: (res) => {
        this.allInvoices = res.data.map((invoice: any) => {
          const userData = JSON.parse(invoice.user_data);
          const orderData = JSON.parse(invoice.order_data);
          return {
            ...invoice,
            userData,
            orderData
          };
        });
      }
    });
  }
  selectOrderDetails: any = null;
  isOrderDetailsVisible: boolean = false;

  showOrderDetails(order: any) {
    this.selectOrderDetails = order;
    this.isOrderDetailsVisible = true;
  }

  dealerDialogVisible: boolean = false;
  selectedDealer: any = null;
  showDealerDetails(dealer: any) {
    this.selectedDealer = dealer;
    this.dealerDialogVisible = true;
  }

  get formattedAddress(): string {
    if (this.selectedDealer?.address_payload) {
      const address = JSON.parse(this.selectedDealer.address_payload);
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

  isDeliveryBoyAvailable: boolean = false;
  availableDeliveryBoys: any = [];

  checkDeliveryBoyAvailability() {
    this.deliveryBoyService.fetchAllDeliveryBoy().subscribe({
      next: (res) => {
        if (res.staff && Array.isArray(res.staff)) {
          this.availableDeliveryBoys = res.staff.filter((boy: any) => boy.order_id === null);
          if (this.availableDeliveryBoys.length > 0) {
            this.isDeliveryBoyAvailable = true;
          } else {
            this.isDeliveryBoyAvailable = false;
          }
        }
      },
      error: (err) => {
        console.log(err);
      }
    });
  }

  isDeliveryBoyModalVisible: boolean = false;
  selectedDeliveryBoy: any = null;

  openDeliveryBoySelection() {
    this.isDeliveryBoyModalVisible = true;
  }

  markAsShipped(order: any, deliveryBoyId: number) {
    this.loadingService.show();
    if (!deliveryBoyId) {
      this.showMessage('warn', 'Warn', 'Please select a delivery boy first!')
      return;
    }

    this.orderService.updateOrderStatus(order.orderId, 'Shipped', deliveryBoyId).subscribe(() => {
      order.status = 'Shipped';
      this.isOrderDetailsVisible = false;
      this.isDeliveryBoyModalVisible = false;
      this.showMessage('warn', 'Warn', `Order has been shipped successfully and assigned to ${this.selectedDeliveryBoy.name}!`)
      this.refreshData()
      this.loadingService.hide();
    });
  }

  staffList: any[] = [];
  staffDialogVisible: boolean = false;
  isAddMode: boolean = true;
  staffForm: any = {
    name: '',
    phone: '',
    alternate_phone: '',
    address: '',
    staff_type: '',
  };
  staffTypes = [
    { label: 'Manager', value: 'Manager' },
    { label: 'Clerk', value: 'Clerk' },
    { label: 'Delivery', value: 'Delivery' },
    { label: 'Support', value: 'Support' }
  ];

  loadStaff() {
    this.userService.fetchAllStaff().subscribe({
      next: (res) => {
        this.staffList = res.staff
      }
    });
  }

  openStaffDialog(mode: string, staff: any = null) {
    this.isAddMode = mode === 'add';
    if (mode === 'update' && staff) {
      this.staffForm = { ...staff };  // Pre-fill the form for update
    } else {
      this.staffForm = {
        name: '',
        phone: '',
        alternate_phone: '',
        address: '',
        staff_type: ''
      };  // Clear the form for adding a new staff
    }
    this.staffDialogVisible = true;
  }

  saveStaff() {
    if (this.isAddMode) {
      this.staffForm.staff_type = this.staffForm.staff_type.value;
      this.userService.insertStaff(this.staffForm).subscribe(() => {
        this.loadStaff();
        this.showMessage('success', 'Success', 'Staff Added!!!')
        this.staffDialogVisible = false;
      });
    } else {
      this.staffForm.staff_type = this.staffForm.staff_type.value;
      this.userService.updateStaff(this.staffForm).subscribe(() => {
        this.loadStaff();
        this.showMessage('success', 'Success', 'Staff Updated!!!')
        this.staffDialogVisible = false;
      });
    }
  }

  deleteStaff(id: number) {
    this.userService.deleteStaff(id).subscribe(() => {
      this.loadStaff();
      this.showMessage('warn', 'Warn', 'Staff Deleted!!!')
    });
  }

  resetStaffForm() {
    this.staffForm = {
      name: '',
      phone: '',
      alternate_phone: '',
      address: '',
      staff_type: '',
      is_available: true,
    };
  }

  showMessage(strSeverity: string, strSummary: string, strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }

  async downloadInvoicePDF(invoice: any) {
    const doc = new jsPDF();

    // Parse the user_data and order_data strings to JSON objects
    const userData = JSON.parse(invoice.user_data);
    const orderData = JSON.parse(invoice.order_data);

    // Header background
    doc.setFillColor(180, 180, 180); // Slightly darker gray background
    doc.rect(0, 0, doc.internal.pageSize.width, 30, 'F');
    doc.setFontSize(18);
    doc.setTextColor(40, 40, 40);
    doc.text(this.companyDetails.name || 'Company Name', 15, 20);

    doc.setFontSize(12);
    doc.text(`Invoice ID: ${invoice.id}`, 15, 35);
    doc.text(`Customer: ${userData.username}`, 15, 45);
    doc.text(`Shop Name: ${userData.shop_name}`, 15, 55);
    doc.text(`Email: ${userData.email}`, 15, 65);
    doc.text(`Order Date: ${orderData.order_date}`, 15, 75);

    // Status with color background
    doc.setFillColor(orderData.status === 'Delivered' ? 46 : 255, orderData.status === 'Pending' ? 204 : 204, 113); // Green for paid, yellow for pending
    doc.rect(15, 90, 50, 8, 'F');
    doc.setTextColor(255);
    doc.text(`Order Status: ${orderData.status}`, 18, 96);
    doc.setTextColor(0);

    // Order items table
    autoTable(doc, {
      startY: 105,
      head: [['Product Name', 'Quantity', 'Price', 'Subtotal']],
      headStyles: { fillColor: [100, 100, 100] },
      body: orderData.order_items.map((item: any) => [
        item.product_name,
        item.quantity,
        `Rs. ${item.price_at_order}`,
        `Rs. ${item.sub_total}`
      ]),
    });

    // Get last table Y position
    const finalY = (doc as any).lastAutoTable?.finalY || 120;
    doc.setFontSize(12);
    doc.text(`Total Amount: Rs. ${orderData.total_price}`, 15, finalY + 10);

    // Footer background
    doc.setFillColor(180, 180, 180);
    doc.rect(0, doc.internal.pageSize.height - 30, doc.internal.pageSize.width, 30, 'F');
    doc.setFontSize(10);
    doc.text(`Contact: ${this.companyDetails.phone} | ${this.companyDetails.alternate_phone}`, 15, doc.internal.pageSize.height - 20);
    doc.text(`Address: ${this.companyDetails.address}`, 15, doc.internal.pageSize.height - 10);

    doc.save(`Invoice_${invoice.id}.pdf`);
  }

  company: any = {
    name: '',
    email: '',
    phone: '',
    alternate_phone: '',
    address: '',
    company_logo: '',
    founded_in: ''
  };

  updateCompanyDetail = false;

  addCompany() {
    this.userService.insertCompany(this.company).subscribe(() => {
      this.fetchComapnyDetails(); // Refresh after adding
      this.company = { name: '', email: '', phone: '', address: '' }; // Reset form
    });
  }

  editDetails() {
    this.updateCompanyDetail = true;
    this.company = { ...this.companyDetails }; // Populate form with existing details
  }

  updateCompany() {
    this.userService.updateCompany(this.company).subscribe(() => {
      this.fetchComapnyDetails(); // Refresh data
      this.updateCompanyDetail = false;
    });
  }

  cancelEdit() {
    this.updateCompanyDetail = false;
    this.company = { name: '', email: '', phone: '', address: '' };
  }

  deleteDetails() {
    if (confirm('Are you sure you want to delete this company?')) {
      this.loadingService.show();
      this.userService.deleteCompany(this.companyDetails.id).subscribe(() => {
        this.companyDetails = null;
        this.company = { name: '', email: '', phone: '', address: '' };
      });
    }
  }

}
