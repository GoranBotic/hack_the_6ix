import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Observable, fromEvent } from 'rxjs';
import { take, tap, pluck } from 'rxjs/operators';

declare var MediaRecorder: any;

@Component({
  selector: 'app-audio-record',
  templateUrl: './audio-record.component.html',
  styleUrls: ['./audio-record.component.css']
})
export class AudioRecordComponent implements OnInit {
  private audioRecorder;
  private recordings: Observable<any>;
  seconds: number;
  audioURLs = [];

  constructor(private sanitizer: DomSanitizer, private changeDetector: ChangeDetectorRef) {}

  ngOnInit() {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        this.audioRecorder = new MediaRecorder(stream);
        this.recordings = fromEvent(this.audioRecorder, 'dataavailable')
      })
      .catch(error => {
        console.log('CANNOT RECORD: ', error);
      }); 
  }

  onHold(time) {
    this.seconds = Math.round(time / 1000);
  }

  onStart() {
    this.audioRecorder.start();
    this.recordings.pipe(
      take(1),
      pluck('data'),
      tap((data: BlobPart) => {
        let blob = new Blob([data], { type: 'audio/x-mpeg-3' });
        this.audioURLs.push(this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(blob)));
        this.changeDetector.detectChanges();
      })
    ).subscribe();
  }

  onStop() {
    this.audioRecorder.stop();
  }
}
