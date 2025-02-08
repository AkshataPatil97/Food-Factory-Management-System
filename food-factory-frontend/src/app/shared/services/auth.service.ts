import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { environment } from '../../../environments/environment';
import { SIGN_IN_URL } from '../constants';
import { jwtDecode } from 'jwt-decode';  


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  apiUrl = environment.apiUrl;

  constructor(private http: HttpClient, private router: Router) {}

  storeToken(token: string): void {
    localStorage.setItem('auth_token', token);
  }

  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  getUser(): any {
    const token = this.getToken();
    if (token) {
      try {
        return jwtDecode(token)  
      } catch (error) {
        console.error("Invalid token", error);
        return null;
      }
    }
    return null;
  }

  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }

  logout(): void {
    localStorage.removeItem('auth_token');
    this.router.navigate(['/login']);
  }

  loginWithEmailAndPassword(email: string, password: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    let signInUrl = this.apiUrl + SIGN_IN_URL;
    return this.http.post(signInUrl, { email, password }, { headers });
  }
}
