import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ngx-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss'],
})
export class ReportsComponent implements OnInit {

  constructor() { }

  items= [
    {'name': 'Name', 'status': {'alive': 'aaa', 'value': 'status'}, 'lastChecked': 'last Checked'},
    {'name': 'AWS RDS', 'status': {'alive': true, 'value': 'available'}, 'lastChecked': '40 minuts ago'},
    {'name': 'Endpoints', 'status': {'alive': true, 'value': ' available'}, 'lastChecked': '20 minuts ago'},
    {'name': 'AWS cloudWatch', 'status': {'alive': false, 'value': ' unavailable'}, 'lastChecked': '10 minuts ago'}];

  missingImages= [
    {'name': 'Name', 'status': {'alive': 'aaa', 'value': 'status'}, 'lastChecked': 'last Checked'},
    {'name': 'AWS RDS', 'status': {'alive': true, 'value': 'available'}, 'lastChecked': '40 minuts ago'},
    {'name': 'Endpoints', 'status': {'alive': true, 'value': ' available'}, 'lastChecked': '20 minuts ago'},
    {'name': 'AWS cloudWatch', 'status': {'alive': false, 'value': ' unavailable'}, 'lastChecked': '10 minuts ago'}];

  missingMetaTags= [
    {'name': 'Name', 'status': {'alive': 'aaa', 'value': 'status'}, 'lastChecked': 'last Checked'},
    {'name': 'AWS RDS', 'status': {'alive': true, 'value': 'available'}, 'lastChecked': '40 minuts ago'},
    {'name': 'Endpoints', 'status': {'alive': true, 'value': ' available'}, 'lastChecked': '20 minuts ago'},
    {'name': 'AWS cloudWatch', 'status': {'alive': false, 'value': ' unavailable'}, 'lastChecked': '10 minuts ago'}];

  ngOnInit() {
  }

}
