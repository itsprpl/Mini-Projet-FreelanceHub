import { Component } from '@angular/core';

@Component({
  selector: 'page-admin',
  template: `
    <ion-header>
      <ion-toolbar>
        <ion-title>Admin Dashboard</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <p>Pending validations, categories and reports will appear here.</p>
    </ion-content>
  `
})
export class AdminPage {}