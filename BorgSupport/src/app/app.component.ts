import { Component } from '@angular/core';
import { AudioRecordComponent } from './audio-record/audio-record.component';
import { CustomerDataService } from './customer-data-service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {


  selectedFile: File = null;
  response: string = '';
  text: string = '';
  todoText = [];
  msgLoaded: Promise<boolean>;

  audioRecord: AudioRecordComponent;
  

  constructor(private customerService: CustomerDataService) {
  }
  ngOnInit(){
    this.generatePhrases();
  }
  /*
    Simple upload file function on button click
  */
  public onUploadFile(){
    const fd = new FormData();
    fd.append('audio',this.selectedFile);
    this.customerService.postMessage(fd).subscribe(res => {
      console.log(res);
      this.response = res["sentiment"];
      this.text = this.response["text"];
      this.msgLoaded = Promise.resolve(true);
      
    });
    
    //console.log(this.text);
  } 

  generatePhrases(){
    this.todoText.push('Welcome to Borg Support, How can i help you?');
    this.todoText.push('Would you be interested in our new deals?');
  }
 
  onFileSelected(event){
    this.selectedFile = <File>event.target.files[0];
  }

}
