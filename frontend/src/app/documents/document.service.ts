import { Injectable } from '@angular/core';
import {environment} from '../environments/environment';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {

  apiUrl =environment.apiUrl;
  constructor(private http: HttpClient) { }

  token: string='';


  URL = this.apiUrl+'/api/document';


  getDocument(): Observable<any> {
    console.log(this.URL)

    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('access_token') || '';  // or localStorage
    }

    console.log(this.token, 'TOKEN');
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.token}`
    });

    return this.http.get(`${this.URL}/documents`, { headers });
  }
  uploadDocument(file: File, title: string): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`http://localhost:8081/api/document/upload_document?title=${title}`, formData);
  }
}
