// document.module.ts
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
// import {mater}
// import { MaterialModule } from '../shared/material/material.module';
import { DocumentRoutingModule } from './document-routing.module';
import { DocumentHomeComponent } from '../document-home/document-home.component';
import {MaterialModule} from '../../shared/material/material.module';
import {FormsModule} from '@angular/forms';
import {SafePipe} from '../document-home/safe.pipe';

@NgModule({
  declarations: [
    DocumentHomeComponent
  ],
  imports: [
    CommonModule,
    DocumentRoutingModule,
    MaterialModule,
    FormsModule,
    SafePipe
  ],
  exports: [DocumentHomeComponent]
})
export class DocumentModule { }
