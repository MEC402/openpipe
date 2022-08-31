import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'ngx-tag-viewer',
  templateUrl: './tag-viewer.component.html',
  styleUrls: ['./tag-viewer.component.scss'],
})

export class TagViewerComponent implements OnInit {
  @Input() tags;
  @Output() onTagChange = new EventEmitter();

  constructor() {
  }

  ngOnInit() {

  }

  sendTheNewValue(e) {
    this.onTagChange.emit({'tag': e.target.id, 'value': e.target.value});
  }
}