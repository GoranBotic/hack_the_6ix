import { Component } from '@angular/core';
import * as RecordRTC from 'recordrtc';
import { DomSanitizer } from '@angular/platform-browser';
import { CustomerDataService } from '../customer-data-service';

@Component({
  selector: 'app-audio-record',
  templateUrl: './audio-record.component.html',
  styleUrls: ['./audio-record.component.css']
})


export class AudioRecordComponent {

  selectedFile: File = null;
  response: string = '';
  text: string = '';
  msgLoaded: Promise<boolean>;

   //Lets initiate Record OBJ
    private record;
    //Will use this flag for detect recording
    private recording = false;
    //Url of Blob
    private url;
    private error;
    constructor(private domSanitizer: DomSanitizer, private customerService: CustomerDataService) {
    }
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
