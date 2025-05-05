import {Component, OnInit} from '@angular/core';
import {DocumentService} from '../document.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import { MatDialogRef } from '@angular/material/dialog';
@Component({
  selector: 'app-upload-document',
  standalone: false,
  templateUrl: './upload-document.component.html',
  styleUrl: './upload-document.component.css'
})
export class UploadDocumentComponent implements OnInit {
  selectedFile: File | null = null;
  title: string = '';
  showSuccessMessage = false;

  constructor(
    private apiService: DocumentService,
    private snackBar: MatSnackBar,
    private dialogRef: MatDialogRef<UploadDocumentComponent>
  ) {}

  ngOnInit(): void {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFile = input.files?.[0] || null;
  }

  onSubmit(): void {

    console.log(this.selectedFile, "on submit");
    if (this.selectedFile && this.title) {
      this.apiService.uploadDocument(this.selectedFile, this.title).subscribe({
        next: (res) => {
          this.snackBar.open('Document uploaded successfully!', 'Close', {
            duration: 3000,
            panelClass: 'snackbar-success'
          });
          this.showSuccess();
        },
        error: (err) => {
          this.snackBar.open('Failed to upload document!', 'Close', {
            duration: 3000,
            panelClass: 'snackbar-error'
          });
        }
      });
    }
  }

  showSuccess() {
    this.showSuccessMessage = true;
    setTimeout(() => {
      this.showSuccessMessage = false;
      this.closeModal();
    }, 2000);
  }

  closeModal(): void {
    this.dialogRef.close();
  }
}
