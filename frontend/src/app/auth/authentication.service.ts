import { Injectable } from '@angular/core';
import {environment} from '../environments/environment';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  apiUrl =environment.apiUrl;

  URL = this.apiUrl+'/api/auth';

  constructor(private http: HttpClient) { }

  login(username: string, password: string) {
    const loginData = {
      email: username,
      password: password
    };

    return this.http.post(`${this.URL}/login`, loginData);
  }

  registerUser(name: string, email: string, password: string,role_id: number) {
    const userData = {
      full_name: name,
      email: email,
      password: password,
      role_id: role_id
    };
    console.log("Registering user", userData);

    return this.http.post(`${this.URL}/register`, userData);
  }

  getAllRoles() {
    return this.http.get(`${this.apiUrl}/roles`);
  }

}
