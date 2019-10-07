import { Component, OnInit } from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';

@Component({
  selector: 'ngx-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  searchTerm: string;
  metInfo: any;
  source;
  constructor(private dataAccess: DataAccessService) {
    this.source= {'id': '123'};
  }

  ngOnInit() {

  }

  searchAssets() {
    this.dataAccess.getMETsData(this.searchTerm, 0 , 20).subscribe(res => {
      this.metInfo = res;
    });
  }
}
