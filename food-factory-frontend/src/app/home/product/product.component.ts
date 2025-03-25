import { Component, Input, OnInit } from '@angular/core';
import { Product } from '../../shared/interface/product';
import { ProductService } from '../../shared/services/product.service';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss']
})
export class ProductComponent implements OnInit {
  @Input() productAction: string = '';
  products: Product[] = [];

  product_name: string = '';
  product_code: string = '';
  category_id: number | null = null;
  manufacturing_date: string = '';
  expiry_date: string = '';
  price: number = 0;
  showDetails: boolean = false;
  isEditing: boolean = false;
  constructor(
    private productService: ProductService,
    private messageService: MessageService
  ) {}

  categoryOptions = [
    { name: 'Electronics', value: 1 },
    { name: 'Clothing', value: 2 },
    { name: 'Food', value: 3 }
  ];

  ngOnInit(): void {
    this.fetchAllProducts();
  }

  fetchAllProducts() {
    this.productService.fetchAllProduct().subscribe({
      next: (response: any) => {
        if (response.data) {
          this.products = this.mapProducts(response.data);
        } else {
          console.error("Invalid response structure:", response);
        }
      },
      error: (error) => {
        console.error("Error fetching products:", error);
      }
    });
  }


  mapProducts(data: any[]): Product[] {
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

  onSubmit() {
    const formData = this.createProductFormData(
      this.product_name, this.product_code, this.category_id,
      this.manufacturing_date, this.expiry_date, this.price, this.showDetails, this.isEditing
    );
    this.productService.insertProduct(formData).subscribe(
      res => {
        this.resetForm();
        this.fetchAllProducts(); // Refresh product list after adding new product
      },
      error => {
        console.error('Error during registration:', error);
      }
    );
  }

  resetForm() {
    this.product_name = '';
    this.product_code = '';
    this.category_id = null;
    this.manufacturing_date = '';
    this.expiry_date = '';
    this.price = 0;
  }

  isFormEmpty(): boolean {
    return !this.product_name && !this.product_code && !this.category_id &&
      !this.manufacturing_date && !this.expiry_date && !this.price;
  }

  createProductFormData(
    product_name: string,
    product_code: string,
    category_id: number | null,
    manufacturing_date: string,
    expiry_date: string,
    price: number,
    showDetails: boolean,
    isEditing: boolean
  ): Product {
    return { product_name, product_code, category_id, manufacturing_date, expiry_date, price, showDetails, isEditing };
  }

  viewProduct(product: Product) {
    product.showDetails = !product.showDetails;
  }

  updateProduct(productCode: string) {
    const selectedProduct = this.products.find(p => p.product_code === productCode);
    if (selectedProduct) {
      this.product_name = selectedProduct.product_name;
      this.product_code = selectedProduct.product_code;
      this.category_id = selectedProduct.category_id;
      this.manufacturing_date = selectedProduct.manufacturing_date;
      this.expiry_date = selectedProduct.expiry_date;
      this.price = selectedProduct.price;
      this.isEditing = true;
    }
  }

  onUpdate() {
    const updatedData = this.createProductFormData(
      this.product_name, this.product_code, this.category_id,
      this.manufacturing_date, this.expiry_date, this.price, false, false
    );
    this.productService.updateProduct(updatedData).subscribe(
      res => {
        console.log('Product updated successfully:', res);
        this.resetForm();
        this.fetchAllProducts(); 
        this.isEditing = false; 
      },
      error => {
        console.error('Error updating product:', error);
      }
    );
  }


  deleteProduct(productCode: string) {
    console.log('Delete Product:', productCode);
    this.productService.deleteProduct(productCode).subscribe(response => {
      console.log('Product deleted successfully:', response);
      this.fetchAllProducts(); // Refresh the product list after deletion
    }, error => {
      console.error('Error deleting product:', error);
    });
    
  }

  visible: boolean = false;

  showConfirm() {
      if (!this.visible) {
          this.messageService.add({ key: 'confirm', sticky: true, severity: 'success', summary: 'Can you send me the report?' });
          this.visible = true;
      }
  }

  onConfirm() {
      this.messageService.clear('confirm');
      this.visible = false;
  }

  onReject() {
      this.messageService.clear('confirm');
      this.visible = false;
  }
}
