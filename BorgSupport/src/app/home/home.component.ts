import { Component, OnInit } from '@angular/core';
import { CustomerDataService } from '../customer-data-service';
import { AudioRecordComponent } from '../audio-record/audio-record.component';
import * as RecordRTC from 'recordrtc';
import { DomSanitizer } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})

export class HomeComponent implements OnInit {

  selectedFile: File = null;
  response: string = '';
  text: string = '';
  msgLoaded: Promise<boolean>;

  audioRecord: AudioRecordComponent;
  

  constructor(private customerService: CustomerDataService) {
  }
  ngOnInit(){

  }
  /*
    Simple upload file function on button click
  */
  public onUploadFile(){
    const fd = new FormData();
    fd.append('audio',this.selectedFile);
    this.customerService.postMessage(fd).subscribe(res => {
      console.log(res);
      this.response = res["sentinment"];
      this.text = this.response["text"];
      this.msgLoaded = Promise.resolve(true);
    });
    
    //console.log(this.text);
  } 

 
  onFileSelected(event){
    this.selectedFile = <File>event.target.files[0];
  }

}
