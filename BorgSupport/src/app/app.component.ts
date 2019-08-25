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
  texts = [];
  todoText = [];
  msgLoaded: Promise<boolean>;
  sentiment : number;

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
      this.texts.push(this.response["text"]);
      this.msgLoaded = Promise.resolve(true);
      this.sentiment = this.response["polarity"];
      
    });
    
    //console.log(this.text);
  } 

  generatePhrases(){
    this.todoText.push('Welcome to Borg Support, How can i help you?');
    this.todoText.push('Would you be interested in our new deals?');
    this.todoText.push('How is you day today?');
    this.todoText.push('Technical Service Line (123)-345-6789');
    this.todoText.push('Regular rates are 2 dollars');
    this.todoText.push('Premium rates are 3.5 dollars');

  }
 
  onFileSelected(event){
    this.selectedFile = <File>event.target.files[0];
  }

}
