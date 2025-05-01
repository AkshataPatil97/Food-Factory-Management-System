import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Product } from '../interface/product';
import { Observable } from 'rxjs';
import { DELETE_PRODUCT_URL, FETCH_ALL_PRODUCT_URL, PRODUCT_INSERT_URL, UPDATE_PRODUCT_URL } from '../constants';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  constructor(private http: HttpClient) { }
  apiUrl = environment.apiUrl;

  insertProduct(product: FormData): Observable<any> {
    let insertURL = this.apiUrl + PRODUCT_INSERT_URL;
    return this.http.post(insertURL, product);
  }

  fetchAllProduct(): Observable<Product[]> {
    const fetchURL = this.apiUrl + FETCH_ALL_PRODUCT_URL;
    return this.http.get<Product[]>(fetchURL);
  }

  updateProduct(product: FormData): Observable<any> {
    const updateURL = this.apiUrl + UPDATE_PRODUCT_URL;
    return this.http.put(updateURL, product);
  }

  deleteProduct(product_code: string): Observable<any> {
    const deleteURL = `${this.apiUrl + DELETE_PRODUCT_URL}?code=${product_code}`;
    return this.http.delete(deleteURL);
  }
}
