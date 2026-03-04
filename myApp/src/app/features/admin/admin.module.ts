import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { AdminPage } from './admin.page';

@NgModule({
  declarations: [AdminPage],
  imports: [CommonModule, IonicModule, RouterModule.forChild([{ path: '', component: AdminPage }])]
})
export class AdminModule {}