import { Component, OnInit } from '@angular/core';

interface Message{
  sentiment : [];
  aggregate: []; 
  text: string;
} //structure of a message from user

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css']
})

export class MessagesComponent implements OnInit {

  messages:Array<Message>; //messages that will be displayed on the chat

  constructor(){
      this.messages = []; //create empty array
  }

  ngOnInit() {
  }

}
