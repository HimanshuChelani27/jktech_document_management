import { Component, OnInit } from '@angular/core';
import {  MatTableDataSource } from '@angular/material/table';
import {MatDialog} from "@angular/material/dialog";
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';
import {DocumentService} from '../document.service';
import {UploadDocumentComponent} from '../upload-document/upload-document.component';

interface Document{
  document_id: number,
  title: string,
  file: string,
  filename: string,
  user_id: number,
  // created_at:
}
@Component({
  selector: 'app-document-home',
  standalone: false,
  templateUrl: './document-home.component.html',
  styleUrl: './document-home.component.css'
})
export class DocumentHomeComponent implements OnInit {
  documents: Document[]=[];
  dataSource!: MatTableDataSource<any>;
  username :any ;
  user_id :any ;
  constructor(private dialog: MatDialog, private apiService: DocumentService, private router: Router,private snackBar: MatSnackBar) {}

  ngOnInit(): void {
    if (typeof window !== 'undefined') {
      this.username = sessionStorage.getItem('userName');
      this.user_id = sessionStorage.getItem('userId');
    }

    this.getAllDocuments()
  }
  getAllDocuments() {
    this.apiService.getDocument().subscribe({
      next: (res: any) => {
        this.documents = res.details;
        this.dataSource = new MatTableDataSource(this.documents);
      },
      error: (err) => {
        console.error('Error fetching documents:', err);
      }
    });
  }
  Back(){
    this.router.navigate(['/home']);
  }
  addNewProduct(): void {
    const dialogRef = this.dialog.open(UploadDocumentComponent, {
      width: '400px'
    });
      dialogRef.afterClosed().subscribe((result: any ) => {
      if (result === true) {
        // this.getProductByUser(); // refresh table
      }
    });
  }
}
