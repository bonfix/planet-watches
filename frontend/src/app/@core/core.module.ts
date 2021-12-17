import { CommonModule } from '@angular/common';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { JwtInterceptor, ServerErrorInterceptor } from './interceptors';
import {FormsModule} from "@angular/forms";
import {LoadingInterceptor} from "@core/interceptors/loading.interceptor";

@NgModule({
  declarations: [],
  imports: [CommonModule, HttpClientModule],
  providers: [
    // {
    //   provide: HTTP_INTERCEPTORS,
    //   useClass: ServerErrorInterceptor,
    //   multi: true,
    // },
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: LoadingInterceptor, multi: true },
  ],
})
export class CoreModule {}
