import { Component } from '@angular/core';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-gigs',
  standalone: true,
  imports: [IonHeader, IonToolbar, IonTitle, IonContent],
  template: `
    <ion-header>
      <ion-toolbar>
        <ion-title>Gigs</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      Gigs page works.
    </ion-content>
  `
})
export class GigsPage {}