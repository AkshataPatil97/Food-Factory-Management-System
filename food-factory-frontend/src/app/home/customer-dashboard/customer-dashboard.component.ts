import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';
import { ProductService } from '../../shared/services/product.service';
import { Cart, Product } from '../../shared/interface/product';
import { MessageService } from 'primeng/api';
import { UsersService } from '../../shared/services/users.service';
import { OrdersService } from '../../shared/services/orders.service';

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
  update_order_data: any = {};
  cancel_reason: string = '';
  selectedOrderId: number | null = null;
  activeComponent: 'products' | 'cart' | 'order' | 'profile' | 'settings' | 'checkout' | 'cancel' | null = null;

  constructor(
    private authService: AuthService,
    private productService: ProductService,
    private messageService: MessageService,
    private userService: UsersService,
    private orderService: OrdersService
  ) { }

  ngOnInit(): void {
    this.fetchAllProducts();
    this.setUserId();
    this.fetchUserDetails();
    if (this.userId) {
      this.fetchUserOrdersData(this.userId)
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

  private mapProducts(data: any[]): Product[] {
    return data.map((productArray: any) => ({
      product_name: productArray[1],
      product_code: productArray[2],
      category_id: productArray[3],
      manufacturing_date: productArray[4],
      expiry_date: productArray[5],
      price: productArray[6],
      showDetails: false,
      isEditing: false
    }));
  }

  setActiveComponent(component: 'products' | 'cart' | 'order' | 'profile' | 'settings' | 'checkout' | 'cancel' | null) {
    this.activeComponent = component;
    if (component === 'order'){
      this.fetchUserOrdersData(this.userId)
    }
  }

  addToCart(product: Product) {
    if (this.cart.some(item => item.product.product_code === product.product_code)) {
      this.showMessage('warn', 'Warning', 'Product is already in the cart!');
      return;
    }

    this.cart.push({ product, quantity: 1, sub_total: product.price });
    this.showMessage('success', 'Success', 'Added to cart Successfully');
  }

  updateQuantity(item: Cart, change: number) {
    const index = this.cart.findIndex(cartItem => cartItem.product.product_code === item.product.product_code);
    if (index === -1) return;

    this.cart[index].quantity = Math.max(0, this.cart[index].quantity + change);
    this.cart[index].sub_total = this.cart[index].quantity * this.cart[index].product.price;

    if (this.cart[index].quantity === 0) {
      this.cart.splice(index, 1);
    }
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
          console.log("Order updated successfully!");
          this.showMessage('success', 'Success', 'Order updated successfully');
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
          console.log("Order inserted successfully!");
          this.showMessage('success', 'Success', 'Order placed successfully');
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

  showMessage(severity: string, summary: string, detail: string) {
    this.messageService.add({ severity, summary, detail });
  }

  toggleProductDetails(product: Product) {
    product.showDetails = !product.showDetails;
  }

  fetchUserOrdersData(userId: number) {
    this.orderService.fetchUserOrders(userId).subscribe({
        next: (response: any) => {
            this.fetchUserOrders = response.data; 
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
        alert("Order canceled successfully");
        this.fetchUserOrdersData(this.userId)
        this.activeComponent = 'order';
        this.cancel_reason = '';
        this.selectedOrderId = null;
      }, error: (error) => {
        alert("Failed to cancel order. Please try again.");
      }
    });
    this.fetchUserOrdersData(this.userId)
  }

  logout() {
    this.authService.logout();
  }
}
