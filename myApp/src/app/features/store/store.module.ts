import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { StorePage } from './store.page';

@NgModule({
  declarations: [StorePage],
  imports: [CommonModule, IonicModule, RouterModule.forChild([{ path: '', component: StorePage }])]
})
export class StoreModule {}