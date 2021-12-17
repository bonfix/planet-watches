import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { WebShellModule } from '@shell/web-shell.module';
import { CoreModule } from './@core/core.module';
import { AppComponent } from './app.component';
import {FormsModule} from "@angular/forms";

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, CoreModule, WebShellModule, FormsModule],
  bootstrap: [AppComponent],
})
export class AppModule {}
