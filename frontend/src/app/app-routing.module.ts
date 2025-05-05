import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AuthenticationComponent} from './auth/authentication/authentication.component';
import {HomeComponent} from './home/home.component';

const routes: Routes = [
   { path: '', component: AuthenticationComponent },
  {
    path: 'home', component: HomeComponent
  },
  {
    path: 'document',
    loadChildren: () => import('./documents/document/document.module').then(m => m.DocumentModule)
    // canActivate: [AuthGuard]
  },
  // {
  //   path:'home', component: HomeComponent, canActivate: [AuthGuard]
  // }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
