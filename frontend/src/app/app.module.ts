import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration, withEventReplay } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthenticationComponent } from './auth/authentication/authentication.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import {RouterModule} from '@angular/router';
import { HomeComponent } from './home/home.component';
// import { DocumentHomeComponent } from './documents/document-home/document-home.component';
import {DocumentModule} from './documents/document/document.module';
import { DocumentlistComponent } from './documents/documentlist/documentlist.component';
import {MatDialogModule} from '@angular/material/dialog';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatCardModule} from '@angular/material/card';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatSortModule} from '@angular/material/sort';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatListModule} from '@angular/material/list';
import {MatDividerModule} from '@angular/material/divider';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatChipsModule} from '@angular/material/chips';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatNativeDateModule} from '@angular/material/core';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatTooltipModule} from '@angular/material/tooltip';
import { UploadDocumentComponent } from './documents/upload-document/upload-document.component';
@NgModule({
  declarations: [
    AppComponent,
    AuthenticationComponent,
    HomeComponent,
    DocumentlistComponent,
    UploadDocumentComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    CommonModule,
    RouterModule,
    DocumentModule,
    MatDialogModule,
    MatSnackBarModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule,
    MatSlideToggleModule,
    MatTableModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatCardModule,
    MatSelectModule,
    MatPaginatorModule,
    MatSortModule,
    MatDialogModule,
    MatSnackBarModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    MatDividerModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatExpansionModule,
    MatCheckboxModule,
    MatTooltipModule,
    MatSlideToggleModule,
    FormsModule,
  ],
  providers: [
    provideClientHydration(withEventReplay())
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
