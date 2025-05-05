import { Component } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthenticationService} from '../auth/authentication.service';

@Component({
  selector: 'app-home',
  standalone: false,
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
   ngOnInit(): void {
    // Initialize product data
    this.getAllRolesAPI();
  }
  constructor(private route: ActivatedRoute, private router: Router, private apiService: AuthenticationService) {

  }

  roles: any[] = [];
  getAllRolesAPI(): void {
    this.apiService.getAllRoles().subscribe({
      next: (res: any) => {
        this.roles = res.data; // adjust if your response structure is different
      },
      error: (err) => {
        console.error('Error fetching Roles:', err);
      }
    });
  }
  routetocreate(){
    this.router.navigate(['/document']);
  }
  routeToPriceOptimizer(){
    this.router.navigate(['/product/pricing-optimization']);
  }

}
