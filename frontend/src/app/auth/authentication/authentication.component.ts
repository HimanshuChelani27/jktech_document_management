import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
// import {Router} from 'express';
import {AuthenticationService} from '../authentication.service';
// import { Router } from "@angular/router";
import { Router } from "@angular/router";
@Component({
  selector: 'app-authentication',
  standalone: false,
  templateUrl: './authentication.component.html',
  styleUrl: './authentication.component.css'
})
export class AuthenticationComponent implements OnInit{


  authForm!: FormGroup;
  isLogin: boolean = true;
  loginError: string = '';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private apiService: AuthenticationService
  ) {}

  ngOnInit(): void {
    this.initForm();

      // Initialize product data
      this.getAllRolesAPI();

  }
  roles: any[] = [];
  getAllRolesAPI(): void {
    this.apiService.getAllRoles().subscribe({
      next: (res: any) => {
        this.roles = res.details; // adjust if your response structure is different
      },
      error: (err) => {
        console.error('Error fetching Roles:', err);
      }
    });
  }


  initForm(): void {
    this.authForm = this.fb.group({
      name: [''],
      role: ['admin'],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }
  switchMode(): void {
    this.isLogin = !this.isLogin;
  }

  closeModal(): void {
    // Optional: You can define logic here to close the modal or navigate away
    this.router.navigate(['/']);
  }

  submit(): void {
    this.loginError = '';

    const { email, password, name, role, phone } = this.authForm.value;
    if (this.isLogin) {
      this.apiService.login(email, password).subscribe(
        (response: any) => {
          if (response.code === 200 && response.details?.access_token) {
            const userData = response.details;
            console.log(userData, 'userData');
            console.log(userData.access_token, 'access_token');
            if (typeof window !== 'undefined') {
              localStorage.setItem('access_token', userData.access_token);
              sessionStorage.setItem('token_type', userData.token_type);
            }
            alert('✅ Login successful!');
            this.router.navigate(['/home']).then(success => {
              console.log('Navigation to home:', success);
            });
          } else {
            alert('⚠️ Login failed: ' + (response.message || 'Unknown error'));
          }
        },
        (error: any) => {
          if (error.status === 400 && error.error?.message === 'Incorrect username or password') {
            alert('❌ Invalid email or password. Please try again.');
          } else if (error.status === 403 && error.error?.message === 'Email not verified') {
            alert(error.error.error || '⚠️ Email not verified. Please check your inbox and verify your account.');
          } else if (error.status === 0) {
            alert('🚫 Server is not responding. Please try again later.');
          } else {
            alert('❌ An unexpected error occurred: ' + (error.error?.message || 'Unknown issue'));
          }

          console.error('Login error:', error);
        }
      );

    } else {

      console.log("Else block")
      const selectedRole = this.roles.find(r => r.name === role);
      const role_id = selectedRole?.role_id || 0;

      if (!role_id) {
        this.loginError = 'Invalid role selected.';
        return;
      }

      this.apiService.registerUser(name, email, password, role_id).subscribe(
        (res: any) => {
          console.log("res", res);
          if (res.code === 201) {
            alert('✅ Signup successful! Please verify your email.');
            this.switchMode(); // Switch to login after successful signup
          } else {
            alert('⚠️ Signup failed: ' + (res.message || 'Please try again.'));
          }
        },
        (err: any) => {
          if (err.code === 400 || err.error?.message === 'Username already registered') {
            alert('⚠️ This email is already registered. Please login or use a different email.');
          } else if (err.code === 0) {
            alert('🚫 Server is not responding. Please check your internet or try again later.');
          } else {
            alert('❌ An unexpected error occurred: ' + (err.error?.message || 'Unknown error.'));
          }
          console.error('Signup error:', err);
        }
      );
    }
  }

}
