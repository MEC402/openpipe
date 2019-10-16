import { Component, OnInit } from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';

@Component({
  selector: 'ngx-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  searchTerm: string;
  source= [];
  met= true;
  rijk= true;
  cleveland= true;
  constructor(private dataAccess: DataAccessService) {
  }

  ngOnInit() {

  }

  searchAssets() {
    this.source = [];
    if (this.met) {
      this.dataAccess.getMETsData(this.searchTerm, 0 , 20).subscribe(res => {
        const data = {'name': 'MET Museum', 'data': res};
        this.source.push(data);
        console.log(this.source);
      });
    }

    if (this.rijk) {
      this.dataAccess.getRijksData(this.searchTerm, 0 , 20).subscribe(res => {
        const data = {'name': 'Rijk Museum', 'data': res};
        this.source.push(data);
        console.log(this.source);
      });
    }

    if (this.cleveland) {
      this.dataAccess.getClevelandData(this.searchTerm, 0 , 20).subscribe(res => {
        const data = {'name': 'Cleveland Museum', 'data': res};
        this.source.push(data);
        console.log(this.source);
      });
    }




  }
}
