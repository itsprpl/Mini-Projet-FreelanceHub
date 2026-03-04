import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from './services/api.service';

@NgModule({
  imports: [CommonModule],
  providers: [ApiService]
})
export class CoreModule {}