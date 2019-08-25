import { RouterModule, Router } from '@angular/router';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { AppComponent } from './app.component';
import { MatButtonModule} from '@angular/material/button';
import { HttpClientModule } from '@angular/common/http';
import { MessagesComponent } from './messages/messages.component';
import { CustomerDataService } from './customer-data-service';
import { AudioRecordComponent } from './audio-record/audio-record.component';

@NgModule({
  declarations: [
    AppComponent,
    MessagesComponent,
    AudioRecordComponent,
  ],
  imports: [
    BrowserModule,
    CommonModule,
    BrowserAnimationsModule,
    MatButtonModule,
    HttpClientModule
    
  ],
  providers: [CustomerDataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
