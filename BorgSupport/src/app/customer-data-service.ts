import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CustomerDataService {

  api = ''
  response = '';
  text = '';


  constructor(private http: HttpClient) { }

  postMessage(fd: FormData){
      console.log("Clicked!");
      this.response = '';
      this.text = '';
      return this.http.post('http://35.222.73.50:4500/api/v1/analyze',fd);/*.subscribe(res => {
      this.response = res["sentinment"];
      this.text = this.response["text"];
    });*/
    //return this.text;
  }

  getText() {
    return this.text;
  }
}
