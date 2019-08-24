import { Component } from '@angular/core';
import { CustomerDataService } from './customer-data-service';
import { AudioRecordComponent } from './audio-record/audio-record.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  selectedFile: File = null;
  response: string = '';
  text: string = '';
  msgLoaded: Promise<boolean>;

  audioRecord: AudioRecordComponent;



  constructor(private customerService: CustomerDataService){}

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

}
