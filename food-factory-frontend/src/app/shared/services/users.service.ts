import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RegistrationForm } from '../interface/user';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { FORGOT_PASS_URL, RESET_PASS_URL, USER_INSERT_URL, VERIFY_OTP_URL, FETCH_DEALER_DETAILS_URL, UPDATE_DEALER_DETAILS_URL, FETCH_USER_DETAILS_URL, FETCH_COMPANY_DETAILS_URL, FETCH_ALL_STAFF_URL, INSERT_STAFF_URL, UPDATE_STAFF_URL, DELETE_STAFF_URL, STAFF_LOGIN_URL, STAFF_OTP_URL, STAFF_VERIFY_OTP_URL, INSERT_COMPANY_URL, UPDATE_COMPANY_URL, DELETE_COMPANY_URL } from '../constants';

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

  verifyOTP(email: string, otp: string): Observable<any>{
    let currentTime = new Date().toLocaleString("en-CA", {
      timeZone: "Asia/Kolkata", 
      hour12: false
    }).replace(",", "");
  
    currentTime = currentTime.replace("/", "-").replace("/", "-");
    
    let verifyOTPUrl = this.apiUrl + VERIFY_OTP_URL;
    return this.http.post(verifyOTPUrl, { email, otp, currentTime })
  }

  staffVerifyOTP(email: string, otp: string, order_id: number|null, status: string, staff_id: number|null): Observable<any>{
    let currentTime = new Date().toLocaleString("en-CA", {
      timeZone: "Asia/Kolkata", 
      hour12: false
    }).replace(",", "");
  
    currentTime = currentTime.replace("/", "-").replace("/", "-");
    
    let verifyOTPUrl = this.apiUrl + STAFF_VERIFY_OTP_URL;
    return this.http.post(verifyOTPUrl, { email, otp, currentTime, order_id, status, staff_id })
  }


  resetPassword(email: string, password: string): Observable<any>{
    let resetPassUrl = this.apiUrl + RESET_PASS_URL;
    return this.http.post(resetPassUrl, { email, password })
  }

  fetchDealerData(user_id: number, user_role: string): Observable<any>{
    let fetchDealerDetailsUrl = this.apiUrl + FETCH_DEALER_DETAILS_URL;
    return this.http.post(fetchDealerDetailsUrl, { user_id, user_role })
  }

  updateDealerDetails(update_field: string, update_value: string | number, user_id: number): Observable<any>{
    let updateDealerDetailsUrl = this.apiUrl + UPDATE_DEALER_DETAILS_URL;
    return this.http.post(updateDealerDetailsUrl, { update_field, update_value, user_id })
  }

  fetchUserById(user_id: number): Observable<any>{
    let fetchUserDetailsByIdUrl = this.apiUrl + FETCH_USER_DETAILS_URL;
    return this.http.post(fetchUserDetailsByIdUrl, { user_id })
  }

  fetchCompanyDetails(): Observable<any>{
    let fetchCompanyDetailsURL = this.apiUrl + FETCH_COMPANY_DETAILS_URL;
    return this.http.get(fetchCompanyDetailsURL)
  }

  fetchAllStaff(): Observable<any> {
    let fetchAllStaffURL = this.apiUrl + FETCH_ALL_STAFF_URL;
    return this.http.get(fetchAllStaffURL)
  }

  insertStaff(staff: any): Observable<any> {
    let insertStaffURL = this.apiUrl + INSERT_STAFF_URL;
    return this.http.post(insertStaffURL,staff)
  }

  updateStaff(staff: any): Observable<any> {
    let updateStaffURL = this.apiUrl + UPDATE_STAFF_URL;
    return this.http.put(updateStaffURL,staff)
  }

  deleteStaff(id: number): Observable<any> {
    let deleteStaffURL = this.apiUrl + DELETE_STAFF_URL;
    return this.http.put(deleteStaffURL,{id})
  }

  staffLogin(number: string): Observable<any> {
    let staffLoginURL = this.apiUrl + STAFF_LOGIN_URL;
    return this.http.post(staffLoginURL,{number})
  }

  staffSendOTP(email: string): Observable<any> {
    let staffSendOTPURL = this.apiUrl + STAFF_OTP_URL;
    return this.http.post(staffSendOTPURL,{email})
  }

  insertCompany(company: any): Observable<any> {
    const insertURL = this.apiUrl + INSERT_COMPANY_URL;
    return this.http.post(insertURL, company);
  }

  updateCompany(company: any): Observable<any> {
    const updateURL = this.apiUrl + UPDATE_COMPANY_URL;
    return this.http.put(updateURL, company);
  }

  deleteCompany(id: number): Observable<any> {
    const deleteURL = this.apiUrl + DELETE_COMPANY_URL;
    return this.http.delete(deleteURL, {
      body: { id }
    });
  }
}
