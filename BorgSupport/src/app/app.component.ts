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
  text = [];
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
      this.response = res["sentiment"];
      this.text.push(this.response["text"]);
      this.msgLoaded = Promise.resolve(true);

      li = $("<li></li>");
      
      if(this.response["sentiment"] < -0.5) {
        li.addClass("sad") 
      } else if (this.response["sentiment"] > 0.5) {
        li.addClass("happy") 
      } 

      li.append(text)

      $("#transcript ul:first").append(li) 
      
    });
    
    //console.log(this.text);
  } 

  generatePhrases(){
    this.todoText.push('Welcome to Borg Support, How can i help you?');
  }
 
  onFileSelected(event){
    this.selectedFile = <File>event.target.files[0];
  }

}
