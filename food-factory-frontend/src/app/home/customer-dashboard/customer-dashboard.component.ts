import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';
import { ProductService } from '../../shared/services/product.service';
import { Cart, Product } from '../../shared/interface/product';
import { MessageService } from 'primeng/api';
import { UsersService } from '../../shared/services/users.service';

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

  activeComponent: 'products' | 'cart' | 'profile' | 'settings' | 'checkout' | null = null;

  constructor(
    private authService: AuthService,
    private productService: ProductService,
    private messageService: MessageService,
    private userService: UsersService
  ) { }

  ngOnInit(): void {
    this.fetchAllProducts();
    this.setUserId();
    this.fetchUserDetails();
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

  setActiveComponent(component: 'products' | 'cart' | 'profile' | 'settings' | 'checkout' | null) {
    this.activeComponent = component;
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
      user_id: this.userId,
      total_price: this.getTotalPrice(),
      status: 'Pending',
      order_date: new Date().toISOString(),
      is_cancelled: false,
      cancellation_reason: null,
      order_items: this.cart.map(item => ({
        product_id: item.product.product_code, // Assuming product_code is unique
        quantity: item.quantity,
        price_at_order: item.product.price,
        sub_total: item.sub_total
      }))
    };
  
    // Ensure logging before switching the component
    console.log('--- Order JSON ---');
    console.log(JSON.stringify([order], null, 2)); // Wrap order in an array to ensure it logs as an array
    console.table(order.order_items); // Better view of order items in console
  
    this.setActiveComponent('checkout');
  }
  

  placeOrder() {
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

  logout() {
    this.authService.logout();
  }
}
