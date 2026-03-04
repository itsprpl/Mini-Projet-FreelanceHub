import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton
} from '@ionic/angular/standalone';

import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    FormsModule,
    RouterLink
  ],
  template: `
    <ion-header>
      <ion-toolbar>
        <ion-title>Login</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">

      <ion-item>
        <ion-label position="floating">Email</ion-label>
        <ion-input type="email" [(ngModel)]="email"></ion-input>
      </ion-item>

      <ion-item>
        <ion-label position="floating">Password</ion-label>
        <ion-input type="password" [(ngModel)]="password"></ion-input>
      </ion-item>

      <ion-button expand="full" (click)="login()">
        Login
      </ion-button>

      <ion-button expand="full" fill="clear" routerLink="/auth/register">
        Create account
      </ion-button>

    </ion-content>
  `
})
export class LoginPage {
  email = '';
  password = '';

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    if (!this.email || !this.password) {
      alert('Please fill in both email and password.');
      return;
    }

    const payload = {
      email: this.email,
      password: this.password
    };

    const backendUrl = 'http://localhost:5000/api/auth/login'; // match Flask blueprint

    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    this.http.post(backendUrl, payload, { headers }).subscribe({
      next: (res: any) => {
        alert('Login successful!');
        // Optionally store token in localStorage
        if (res.token) {
          localStorage.setItem('token', res.token);
        }
        this.router.navigate(['/']); // redirect to home or dashboard
      },
      error: (err) => {
        console.error('Login error:', err);
        if (err.status === 401) {
          alert('Invalid credentials.');
        } else if (err.status === 403) {
          alert('Account is blocked.');
        } else if (err.status === 400) {
          alert('Please provide both email and password.');
        } else {
          alert('Login failed. See console for details.');
        }
      }
    });
  }
}