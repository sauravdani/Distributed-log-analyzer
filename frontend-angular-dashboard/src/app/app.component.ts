import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Log } from './models/log.model';
import { LogService } from './services/log.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
  logs: Log[] = [];

  // Filter values
  searchService: string = '';
  searchLevel: string = '';
  searchMessage: string = '';

  private logService = inject(LogService);

  ngOnInit(): void {
    this.logService.getLogs().subscribe({
      next: (data) => (this.logs = data),
      error: (err) => console.error('Error fetching logs:', err),
    });
  }

  filteredLogs(): Log[] {
    return this.logs.filter((log) => {
      return (
        (!this.searchService || log.service.toLowerCase().includes(this.searchService.toLowerCase())) &&
        (!this.searchLevel || log.level === this.searchLevel) &&
        (!this.searchMessage || log.message.toLowerCase().includes(this.searchMessage.toLowerCase()))
      );
    });
  }

  deleteLog(id: number): void {
  if (confirm('Are you sure you want to delete this log?')) {
    this.logService.deleteLog(id).subscribe({
      next: () => {
        this.logs = this.logs.filter(log => log.id !== id);
      },
      error: (err) => {
        console.error('Delete failed:', err);
        alert('Failed to delete log from backend.');
      }
    });
  }
}

}
