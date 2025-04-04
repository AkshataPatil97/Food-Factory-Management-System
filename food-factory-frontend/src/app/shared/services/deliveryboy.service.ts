import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { FETCH_ALL_DELIVERY_BOY_URL } from '../constants';

@Injectable({
  providedIn: 'root'
})
export class DeliveryboyService {

  constructor(private http: HttpClient) { }
  apiUrl = environment.apiUrl;

  fetchAllDeliveryBoy():Observable<any> {
    let fetchAllDeliveryBoyURL = this.apiUrl + FETCH_ALL_DELIVERY_BOY_URL;
    return this.http.get(fetchAllDeliveryBoyURL);
  }

}
