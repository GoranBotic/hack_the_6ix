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
  

  constructor(private domSanitizer: DomSanitizer, private customerService: CustomerDataService) {
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

  /*
    Simple text upload function on button click
  
  public onUploadText(){
    console.log("Clicked!");
    const fd = new FormData();
    fd.append('text','this is not good cody');
    this.http.post('http://100.64.201.66:4500/api/v1/analyze', fd).subscribe(res => {
      console.log(res);
    });
  }
  */
  onFileSelected(event){
    this.selectedFile = <File>event.target.files[0];
  }

 

   //Lets initiate Record OBJ
    private record;
    //Will use this flag for detect recording
    private recording = false;
    //Url of Blob
    private url;
    private error;
    
    sanitize(url:string){
        return this.domSanitizer.bypassSecurityTrustUrl(url);
    }
    /**
     * Start recording.
     */
    initiateRecording() {
        
        this.recording = true;
        let mediaConstraints = {
            video: false,
            audio: true
        };
        navigator.mediaDevices
            .getUserMedia(mediaConstraints)
            .then(this.successCallback.bind(this), this.errorCallback.bind(this));
    }
    /**
     * Will be called automatically.
     */
    successCallback(stream) {
        var options = {
            mimeType: "audio/wav",
            numberOfAudioChannels: 1
        };
        //Start Actual Recording
        var StereoAudioRecorder = RecordRTC.StereoAudioRecorder;
        this.record = new StereoAudioRecorder(stream, options);
        this.record.record();
    }
    /**
     * Stop recording.
     */
    stopRecording() {
        this.recording = false;
        this.record.stop(this.processRecording.bind(this));
    }
    /**
     * processRecording Do what ever you want with blob
     * @param  {any} blob Blog
     */
    processRecording(blob) {
      this.url = URL.createObjectURL(blob);
  
    }
   
    /**
     * Process Error.
     */
    errorCallback(error) {
        this.error = 'Can not play audio in your browser';
    }

    public blobToFile = (theBlob: Blob, fileName:string): File => {
      var b: any = theBlob;
      //A Blob() is almost a File() - it's just missing the two properties below which we will add
      b.lastModifiedDate = new Date();
      b.name = fileName;
  
      //Cast to a File() type
      return <File>theBlob;
  }

}
