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
  IonButton,
  IonSelect,
  IonSelectOption
} from '@ionic/angular/standalone';

import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-register',
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
    IonSelect,
    IonSelectOption,
    FormsModule,
    RouterLink
  ],
  template: `
    <ion-header>
      <ion-toolbar>
        <ion-title>Register</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">

      <ion-item>
        <ion-label position="floating">Full Name</ion-label>
        <ion-input [(ngModel)]="name"></ion-input>
      </ion-item>

      <ion-item>
        <ion-label position="floating">Email</ion-label>
        <ion-input type="email" [(ngModel)]="email"></ion-input>
      </ion-item>

      <ion-item>
        <ion-label position="floating">Password</ion-label>
        <ion-input type="password" [(ngModel)]="password"></ion-input>
      </ion-item>

      <ion-item>
        <ion-label>Role</ion-label>
        <ion-select [(ngModel)]="role">
          <ion-select-option value="freelancer">Freelancer</ion-select-option>
          <ion-select-option value="client">Client</ion-select-option>
          <ion-select-option value="admin">Admin</ion-select-option>
        </ion-select>
      </ion-item>

      <ion-button expand="full" (click)="register()">
        Register
      </ion-button>

      <ion-button expand="full" fill="clear" routerLink="/auth/login">
        Already have an account? Login
      </ion-button>

    </ion-content>
  `
})
export class RegisterPage {
  name = '';
  email = '';
  password = '';
  role: string | null = null;

  constructor(private http: HttpClient, private router: Router) {}

  register() {
    if (!this.email || !this.password || !this.role) {
      alert('Please fill all required fields.');
      return;
    }

    const payload = {
      email: this.email,
      password: this.password,
      role: this.role,
      name: this.name // optional
    };

    const backendUrl = 'http://localhost:5000/api/auth/register'; // match your Flask blueprint

    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    this.http.post(backendUrl, payload, { headers }).subscribe({
      next: (res: any) => {
        alert('Registration successful!');
        this.router.navigate(['/auth/login']);
      },
      error: (err) => {
        console.error('Registration error:', err);
        if (err.status === 409) {
          alert('Email already registered.');
        } else if (err.status === 400) {
          alert('Invalid data. Please check your inputs.');
        } else {
          alert('Registration failed. See console for details.');
        }
      }
    });
  }
}