import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { Log } from '../../../log.model';

@Injectable({
  providedIn: 'root'
})
export class LogService {
  private apiUrl = 'http://localhost:8080/api/logs';
  constructor(private http: HttpClient) { }

  getLogs(): Observable<Log[]> {
    return this.http.get<Log[]>(this.apiUrl);
  }
}
