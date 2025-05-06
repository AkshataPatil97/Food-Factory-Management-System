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
  product_img: File | null = null;
  constructor(
    private productService: ProductService,
    private messageService: MessageService
  ) { }

  categoryOptions = [
    // { name: 'Electronics', value: 1 },
    // { name: 'Clothing', value: 2 },
    { name: 'Food', value: 3 }
  ];

  ngOnInit(): void {
    this.fetchAllProducts();
  }

  fetchAllProducts() {
    this.productService.fetchAllProduct().subscribe({
      next: (response: any) => {
        console.log("Products fetched successfully:", response);

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

  onSubmit() {
    const formData = new FormData();
    formData.append('product_name', this.product_name);
    formData.append('product_code', this.product_code);
    formData.append('category_id', this.category_id?.toString() || '');
    formData.append('manufacturing_date', this.manufacturing_date);
    formData.append('expiry_date', this.expiry_date);
    formData.append('price', this.price.toString());
    if (this.product_img) {
      formData.append('product_img', this.product_img);
    }

    this.productService.insertProduct(formData).subscribe({
      next: () => {
        this.resetForm();
        this.fetchAllProducts();
        this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Product added successfully!' });
      },
      error: (err) => {
        console.error('Error inserting product:', err);
      }
    });
  }

  resetForm() {
    this.product_name = '';
    this.product_code = '';
    this.category_id = null;
    this.manufacturing_date = '';
    this.expiry_date = '';
    this.price = 0;
    this.product_img = null;
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
    isEditing: boolean,
    product_img: File | null = null
  ): Product {
    return { product_name, product_code, category_id, manufacturing_date, expiry_date, price, showDetails, isEditing, product_img };
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
      this.product_img = selectedProduct.product_img;
    }
  }

  onUpdate() {
    const formData = new FormData();
    formData.append('product_name', this.product_name);
    formData.append('product_code', this.product_code);
    formData.append('category_id', this.category_id?.toString() || '');
    formData.append('manufacturing_date', this.manufacturing_date);
    formData.append('expiry_date', this.expiry_date);
    formData.append('price', this.price.toString());

    // Append the new product image if available
    if (this.product_img) {
      formData.append('product_img', this.product_img);
    }

    // Call the updateProduct API
    this.productService.updateProduct(formData).subscribe({
      next: (response) => {
        console.log('Product updated successfully:', response);
        this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Product updated successfully!' });
        this.resetForm();
        this.fetchAllProducts();
        this.isEditing = false;
      },
      error: (err) => {
        console.error('Error updating product:', err);
      }
    });
  }


  deleteProduct(productCode: string) {
    console.log('Delete Product:', productCode);
    this.productService.deleteProduct(productCode).subscribe(response => {
      console.log('Product deleted successfully:', response);
      this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Product deleted successfully!' });
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

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.product_img = input.files[0];
    }
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
