import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {DocumentHomeComponent} from '../document-home/document-home.component';

const routes: Routes = [
  { path: '', component: DocumentHomeComponent },
  // { path: 'pricing-optimization', component: PricingOptimizationComponent },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DocumentRoutingModule { }
