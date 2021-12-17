import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FooterModule } from '../footer/footer.module';
import { HeaderModule } from '../header/header.module';
import { LayoutComponent } from './layout.component';
import {FormsModule} from "@angular/forms";

@NgModule({
  declarations: [LayoutComponent],
  imports: [CommonModule, HeaderModule, FooterModule, FormsModule],
  exports: [LayoutComponent],
})
export class LayoutModule {}
