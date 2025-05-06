import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';
import { ProductService } from '../../shared/services/product.service';
import { Cart, Product } from '../../shared/interface/product';
import { MessageService } from 'primeng/api';
import { UsersService } from '../../shared/services/users.service';
import { OrdersService } from '../../shared/services/orders.service';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

@Component({
  selector: 'app-customer-dashboard',
  templateUrl: './customer-dashboard.component.html',
  styleUrls: ['./customer-dashboard.component.scss']
})
export class CustomerDashboardComponent {
  products: Product[] = [];
  cart: Cart[] = [];

  userId: number = 0;
  userName: string = '';
  userRole: string = '';
  order_data: any = {};
  isUpdateOrder: boolean = false;
  fetchUserOrders: any = [];
  fetchUserOrdersHistory: any = [];
  update_order_data: any = {};
  cancel_reason: string = '';
  selectedOrderId: number | null = null;
  companyDetails: any = {};
  activeComponent: string = '';
  sortedOrders = [];
  totalActiveOrdersCount: number = 0;

  constructor(
    private authService: AuthService,
    private productService: ProductService,
    private messageService: MessageService,
    private userService: UsersService,
    private orderService: OrdersService
  ) { }

  ngOnInit(): void {
    this.setActiveComponent('products');
    this.fetchComapnyDetails()
    this.fetchAllProducts();
    this.setUserId();
    this.fetchUserDetails();
    this.refereshData()
  }

  refereshData() {
    if (this.userId) {
      this.fetchUserOrdersData(this.userId)
      this.fetchInvoices()
    }
  }

  private setUserId() {
    const user = this.authService.getUser();
    if (user?.user_id) {
      this.userId = user.user_id;
      this.userRole = user.role;
    }
  }

  private fetchUserDetails() {
    this.userService.fetchUserById(this.userId).subscribe({
      next: (res) => {
        this.userName = res.user_details?.username || 'Guest';
      },
      error: (error) => console.error("Error fetching user details:", error)
    });
  }

  private fetchAllProducts() {
    this.productService.fetchAllProduct().subscribe({
      next: (response: any) => {
        this.products = response.data ? this.mapProducts(response.data) : [];
      },
      error: (error) => console.error("Error fetching products:", error)
    });
  }

  mapProducts(data: any[]): Product[] {
    return data.map((product: any) => ({
      product_name: product.product_name,
      product_code: product.product_code,
      category_id: product.category_id,
      manufacturing_date: product.manufacturing_date,
      expiry_date: product.expiry_date,
      price: product.price,
      showDetails: false,
      isEditing: false,
      product_img: product.product_img ? product.product_img : null
    }));
  }

  fetchComapnyDetails() {
    this.userService.fetchCompanyDetails().subscribe({
      next: (res) => {
        this.companyDetails = res.data;
        console.log(this.companyDetails);

      }
    })
  }

  setActiveComponent(component: string) {
    this.activeComponent = component;
  }

  isActiveComponent(component: string): boolean {
    return this.activeComponent === component;
  }

  addToCart(product: Product) {
    if (this.cart.some(item => item.product.product_code === product.product_code)) {
      this.showMessage('warn', 'Warning', 'Product is already in the cart!');
      return;
    }

    const quantity = 15;
    this.cart.push({
      product,
      quantity,
      sub_total: quantity * product.price
    });

    this.showMessage('success', 'Success', 'Added to cart Successfully');
  }


  updateQuantity(item: Cart, change: number) {
    const index = this.cart.findIndex(cartItem => cartItem.product.product_code === item.product.product_code);
    if (index === -1) return;

    const updatedQuantity = this.cart[index].quantity + change;

    if (updatedQuantity < 15) {
      this.showMessage('warn', 'Warning', 'You cannot select less than 15 kg.');
      return;
    }

    this.cart[index].quantity = updatedQuantity;
    this.cart[index].sub_total = updatedQuantity * this.cart[index].product.price;
  }



  removeFromCart(item: Cart) {
    this.cart = this.cart.filter(cartItem => cartItem.product.product_code !== item.product.product_code);
  }

  getTotalPrice(): number {
    return this.cart.reduce((total, item) => total + item.sub_total, 0);
  }

  checkout() {
    if (this.cart.length === 0) {
      alert('Your cart is empty!');
      return;
    }

    const order = {
      order_id: this.isUpdateOrder ? this.update_order_data.order_id : null,
      user_id: this.userId,
      total_price: this.getTotalPrice(),
      status: 'Pending',
      order_date: new Date().toISOString(),
      is_cancelled: false,
      cancellation_reason: null,
      order_items: this.cart.map(item => ({
        product_id: item.product.product_code,
        quantity: item.quantity,
        price_at_order: item.product.price,
        sub_total: item.sub_total
      }))
    };

    this.order_data = order;
    this.setActiveComponent('checkout');
  }

  order_handling() {
    if (this.isUpdateOrder) {
      this.orderService.updateOrder(this.order_data).subscribe({
        next: () => {
          this.showMessage('success', 'Success', 'Order updated successfully');
          this.refereshData()
          this.isUpdateOrder = false;
        },
        error: (error) => {
          console.error("Error updating order:", error);
          this.showMessage('error', 'Error', 'Failed to update order');
        }
      });
    } else {
      this.orderService.insertOrder(this.order_data).subscribe({
        next: () => {
          this.showMessage('success', 'Success', 'Order placed successfully');
          this.refereshData()
        },
        error: (error) => {
          console.error("Error inserting order:", error);
          this.showMessage('error', 'Error', 'Failed to place order');
        }
      });
    }
  }
  updateOrder(order: any) {
    this.update_order_data = {
      order_id: order.order_id,
      ...order
    };
    this.isUpdateOrder = true;
    this.cart = order.order_items.map((item: any) => ({
      product: {
        product_name: item.product_name,
        product_code: item.product_id,
        manufacturing_date: '',
        expiry_date: '',
        price: item.price_at_order
      },
      quantity: item.quantity,
      sub_total: item.sub_total
    }));
    this.activeComponent = 'cart';
  }


  placeOrder() {
    this.order_handling()
    console.log("Order placed successfully!");
    this.cart = [];
    this.setActiveComponent('products');
  }

  showMessage(strSeverity: string, strSummary: string, strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }

  toggleProductDetails(product: Product) {
    product.showDetails = !product.showDetails;
  }


  fetchUserOrdersData(userId: number) {
    this.orderService.fetchUserOrders(userId).subscribe({
      next: (response: any) => {
        const orders = response.data || [];
        // Separate orders
        const deliveredOrders = orders.filter((order: any) => order.status === 'Delivered');
        const activeOrders = orders.filter((order: any) => order.status !== 'Delivered');

        this.fetchUserOrders = activeOrders.sort((a: any, b: any) =>
          new Date(b.order_date).getTime() - new Date(a.order_date).getTime()
        );
        this.fetchUserOrdersHistory = deliveredOrders.sort((a: any, b: any) =>
          new Date(b.order_date).getTime() - new Date(a.order_date).getTime()
        );

        this.calculateTotalActiveOrders();
      },
      error: (error) => console.error("Error fetching orders:", error)
    });
  }


  cancelOrder(order_id: number) {
    this.activeComponent = 'cancel';
    this.selectedOrderId = order_id;
  }

  confirmCancel() {
    if (!this.cancel_reason || !this.selectedOrderId) {
      alert("Please enter a cancellation reason.");
      return;
    }
    this.orderService.cancelOrder(this.selectedOrderId, this.cancel_reason, this.userId).subscribe({
      next: (response) => {
        this.showMessage('warn', 'Warn', 'Order canceled successfully!!!');
        this.fetchUserOrdersData(this.userId)
        this.activeComponent = 'order';
        this.cancel_reason = '';
        this.selectedOrderId = null;
        this.refereshData()
      }, error: (error) => {
        this.showMessage('error', 'Error', 'Failed to cancel order. Please try again!!!');
      }
    });
    this.fetchUserOrdersData(this.userId)
  }

  logout() {
    this.authService.logout();
  }
  userInvoices: any = {};
  fetchInvoices() {
    this.orderService.fetchInvoicesForUser(this.userId).subscribe({
      next: (res) => {
        console.log(res.data);
        this.userInvoices = res.data.map((invoice: any) => {
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

  calculateTotalActiveOrders() {
    const validStatuses = ['Pending', 'Processing', 'Processed', 'Shipped'];
    this.totalActiveOrdersCount = this.fetchUserOrders.filter((order: any) =>
      validStatuses.includes(order.status)
    ).length;
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
    doc.setFillColor(orderData.status === 'PAID' ? 46 : 255, orderData.status === 'PAID' ? 204 : 204, 113); // Green for paid, yellow for pending
    doc.rect(15, 90, 50, 8, 'F');
    doc.setTextColor(255);
    doc.text(`Status: ${orderData.status}`, 18, 96);
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

  searchTerm: string = '';

  filteredProducts() {
    if (!this.searchTerm) {
      return this.products;
    }
    return this.products.filter(product =>
      product.product_name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }


}
