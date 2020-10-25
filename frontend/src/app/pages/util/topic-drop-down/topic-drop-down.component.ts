import {Component, Input, OnInit} from '@angular/core';
import {DefaultEditor} from 'ng2-smart-table';
import {DataAccessService} from '../../../services/data-access.service';


@Component({
  selector: 'ngx-topic-drop-down',
  templateUrl: './topic-drop-down.component.html',
  styleUrls: ['./topic-drop-down.component.scss'],
})
export class TopicDropDownComponent extends DefaultEditor implements OnInit {
  myValues = [];

  constructor(private dataAccess: DataAccessService) {
    super();
  }

  @Input() value;

  selectedValue: string = '';
  customTagName;

  // rendered as this.yourModelStore = ['value', 'value'];

  ngOnInit() {
    this.dataAccess.currentMessage.subscribe(message =>  {
      this.myValues  = Object.keys(message);
    });
  }

  selectChangeHandler(event) {
    if (event.target.value != 'others') {
      this.cell.newValue = 'openpipe_canonical_' + event.target.value;
    }
  }

  onWrite(event) {
    this.cell.newValue = this.customTagName;
  }
}
