export interface Order {
    orderId: number;
    date: string;
    totalPrice: number;
    status: string;
    order_items: [];
}
  
export interface CancelledOrder {
    reason: string;
    date: string;
    totalPrice: number;
    status: string;
}
