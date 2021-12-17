import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { WebShellModule } from '@shell/web-shell.module';
import { CoreModule } from './@core/core.module';
import { AppComponent } from './app.component';
import {FormsModule} from "@angular/forms";
import { initializeApp,provideFirebaseApp } from '@angular/fire/app';
import { environment } from '../environments/environment';

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, CoreModule, WebShellModule, FormsModule,
    // provideFirebaseApp(() => initializeApp(environment.firebase)),
    // provideAnalytics(() => getAnalytics()),
    // providePerformance(() => getPerformance())
  ],
  bootstrap: [AppComponent],
  providers: [
    // ScreenTrackingService,UserTrackingService
  ],
})
export class AppModule {}
