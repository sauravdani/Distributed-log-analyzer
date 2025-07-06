import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Log } from '../../log.model';
import { LogService } from './services/log.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit{
  logs: Log[] = [];

  constructor(private logService: LogService) {}

  ngOnInit() {
    this.logService.getLogs().subscribe({
      next: (data) => this.logs = data,
      error: (err) => console.error('Error fetching logs', err)
    });
  }
}
