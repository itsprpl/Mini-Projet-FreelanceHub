import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { GigsPage } from './gigs.page';

@NgModule({
  declarations: [GigsPage],
  imports: [CommonModule, IonicModule, RouterModule.forChild([{ path: '', component: GigsPage }])]
})
export class GigsModule {}