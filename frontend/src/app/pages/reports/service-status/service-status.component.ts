import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'ngx-service-status',
  templateUrl: './service-status.component.html',
  styleUrls: ['./service-status.component.scss'],
})
export class ServiceStatusComponent implements OnInit {

  @Input() items;
  constructor() { }

  ngOnInit() {
  }

}
