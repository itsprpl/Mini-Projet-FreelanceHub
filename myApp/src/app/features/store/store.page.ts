import { Component, OnInit } from '@angular/core';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonItem,
  IonLabel,
  IonButton
} from '@ionic/angular/standalone';

import { NgFor } from '@angular/common';

@Component({
  selector: 'app-store',
  standalone: true,
  imports: [
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonList,
    IonItem,
    IonLabel,
    IonButton,
    NgFor
  ],
  template: `
    <ion-header>
      <ion-toolbar>
        <ion-title>Store</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-list>
        <ion-item *ngFor="let p of products">
          <ion-label>
            <h2>{{ p.title }}</h2>
            <p>{{ p.version }} — {{ p.price }} USD</p>
          </ion-label>
          <ion-button fill="outline" (click)="purchase(p)">
            Buy
          </ion-button>
        </ion-item>
      </ion-list>
    </ion-content>
  `
})
export class StorePage implements OnInit {

  products = [
    { id: '1', title: 'Angular Starter Kit', version: '1.0', price: 25 },
    { id: '2', title: 'Flask API Boilerplate', version: '1.2', price: 30 }
  ];

  ngOnInit() {}

  purchase(product: any) {
    alert('Purchased: ' + product.title);
  }
}