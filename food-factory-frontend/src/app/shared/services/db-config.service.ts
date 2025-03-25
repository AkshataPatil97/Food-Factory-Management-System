import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { FETCH_DB_CONFIG_URL, UPDATE_DB_CONFIG_URL } from '../constants';

@Injectable({
  providedIn: 'root'
})
export class DbConfigService {

  constructor(private http: HttpClient) { }
  apiUrl = environment.apiUrl;

  fetchDBConfig(db_config: string): Observable<any> {
    let fetchDbConfigURL = this.apiUrl + FETCH_DB_CONFIG_URL;
    return this.http.post(fetchDbConfigURL, { db_config })
  }

  updateDBConfig(mapFrom: string, mapTo: string): Observable<any> {
    let updateDbConfigURL = this.apiUrl + UPDATE_DB_CONFIG_URL;
    return this.http.post(updateDbConfigURL, { mapFrom, mapTo })
  }
}
