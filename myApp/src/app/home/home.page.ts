import { Component } from '@angular/core';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButton
} from '@ionic/angular/standalone';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonButton,
    RouterLink
  ],
  template: `
    <ion-header>
      <ion-toolbar>
        <ion-title>FreelanceHub</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <ion-button expand="full" routerLink="/gigs">
        Browse Gigs
      </ion-button>

      <ion-button expand="full" routerLink="/store">
        Visit Store
      </ion-button>
      <ion-button expand="full" routerLink="/auth/login">
  Login
</ion-button>
<ion-button expand="full" routerLink="/auth/register">
  Register
</ion-button>
    </ion-content>
  `
})
export class HomePage {}