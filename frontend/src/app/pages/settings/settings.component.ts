import { Component, OnInit } from '@angular/core';
import {DataAccessService} from "../../services/data-access.service";

@Component({
  selector: 'ngx-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {

  constructor(private da: DataAccessService) {
  }

  ngOnInit() {
  }

}
