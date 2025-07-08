import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Log } from './models/log.model';
import { LogService } from './services/log.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
  logs: Log[] = [];

  private logService = inject(LogService); // ✅ Modern DI

  ngOnInit(): void {
    this.logService.getLogs().subscribe({
      next: (data) => (this.logs = data),
      error: (err) => console.error('Error fetching logs:', err),
    });
  }
}
