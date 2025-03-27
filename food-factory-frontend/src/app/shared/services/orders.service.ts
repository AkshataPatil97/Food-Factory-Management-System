import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { CANCEL_USER_ORDER_URL, FETCH_ALL_CANCELLED_ORDER_FOR_ADMIN_URL, FETCH_ALL_DELIVERED_ORDER_FOR_ADMIN_URL, FETCH_ALL_ORDER_FOR_ADMIN_URL, FETCH_USER_ORDERS_URL, ORDER_INSERT_URL, UPDATE_ORDER_STATUS_URL, UPDATE_ORDER_URL } from '../constants';

@Injectable({
  providedIn: 'root'
})
export class OrdersService {

  constructor(private http: HttpClient) { }
  apiUrl = environment.apiUrl;

  insertOrder(order: any): Observable<any> {
    let insertURL = this.apiUrl + ORDER_INSERT_URL;
    return this.http.post(insertURL, order);
  }

  fetchUserOrders(user_id: number): Observable<any> {
    let fetchUserOrdersURL = this.apiUrl + FETCH_USER_ORDERS_URL;
    return this.http.post(fetchUserOrdersURL, {user_id});
  }

  cancelOrder(order_id: number, cancel_reason: string, user_id: number): Observable<any> {
    let cancelOrderURL = this.apiUrl + CANCEL_USER_ORDER_URL;
    return this.http.post(cancelOrderURL, {order_id,cancel_reason,user_id});
  }

  updateOrder(order_data: any): Observable<any> {
    let updateOrderURL = this.apiUrl + UPDATE_ORDER_URL;
    return this.http.put(updateOrderURL, order_data);
  }

  updateOrderStatus(order_id: number, status: string): Observable<any> {
    let updateOrderStatusURL = this.apiUrl + UPDATE_ORDER_STATUS_URL;
    return this.http.put(updateOrderStatusURL, {order_id,status});
  }

  fetchAllOrderForAdmin(): Observable<any> {
    let fetchAllOrdersURL = this.apiUrl + FETCH_ALL_ORDER_FOR_ADMIN_URL;
    return this.http.get(fetchAllOrdersURL);
  }

  fetchAllDeliveredOrderForAdmin(): Observable<any> {
    let fetchAllDeliveredOrdersURL = this.apiUrl + FETCH_ALL_DELIVERED_ORDER_FOR_ADMIN_URL;
    return this.http.get(fetchAllDeliveredOrdersURL);
  }

  fetchAllCancelledOrderForAdmin(): Observable<any> {
    let fetchAllCancelledOrdersURL = this.apiUrl + FETCH_ALL_CANCELLED_ORDER_FOR_ADMIN_URL;
    return this.http.get(fetchAllCancelledOrdersURL);
  }

}
