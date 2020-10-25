import {Component, Input, OnInit} from '@angular/core';
import {DataAccessService} from "../../../services/data-access.service";
import {DefaultEditor} from "ng2-smart-table";

@Component({
  selector: 'ngx-cell-drop-down',
  templateUrl: './cell-drop-down.component.html',
  styleUrls: ['./cell-drop-down.component.scss']
})


export class CellDropDownComponent extends DefaultEditor implements OnInit {
  myValues = [];

  constructor(private dataAccess: DataAccessService) {
    super();
  }

  @Input() value;

  selectedValue: string = '';

  ngOnInit() {
    this.dataAccess.currentSampleTags.subscribe(message =>  {
      this.myValues  = message;
    });
  }

  selectChangeHandler(event) {
      this.cell.newValue = event.target.value;
  }

}
