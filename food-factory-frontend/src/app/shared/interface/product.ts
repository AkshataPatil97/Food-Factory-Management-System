export interface Product {
    product_name: string;
    product_code: string;
    category_id: number | null;
    manufacturing_date: string;
    expiry_date: string;
    price: number;
    showDetails: boolean;
    isEditing: boolean;
    product_img: File | null;
}

export interface Cart {
    sub_total: number;
    product: Product,
    quantity: number
}