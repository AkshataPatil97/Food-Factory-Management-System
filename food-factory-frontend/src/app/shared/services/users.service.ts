import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RegistrationForm } from '../interface/user';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { FORGOT_PASS_URL, USER_INSERT_URL } from '../constants';

@Injectable({
  providedIn: 'root'
})
export class UsersService {

  constructor(private http: HttpClient) { }
  apiUrl = environment.apiUrl;

  insertUser(user: RegistrationForm): Observable<any> {
    let insertURL = this.apiUrl + USER_INSERT_URL;
    return this.http.post(insertURL, user);
  }

  verifyEmailSendOtp(email: string):Observable<any>{
    let forgotPasswordURL = this.apiUrl + FORGOT_PASS_URL;
    return this.http.post(forgotPasswordURL, { email })
  }

}
