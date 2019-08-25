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

import { HomeComponent } from './home/home.component';
import { IntroComponent } from './intro/intro.component';

@NgModule({
  declarations: [
    AppComponent,
    MessagesComponent,
    AudioRecordComponent,
    IntroComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatButtonModule,
    HttpClientModule,
    RouterModule.forRoot([
      {path: '', component: HomeComponent},
      {path: 'intro',component: AudioRecordComponent}
    ])
    
  ],
  providers: [CustomerDataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
