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
  local= true;
  constructor(private dataAccess: DataAccessService) {
  }

  ngOnInit() {

  }

  searchAssets() {
    this.source = [];
    if (this.met) {
      // this.dataAccess.getMETsData(this.searchTerm, 0 , 20).subscribe(res => {
      this.dataAccess.getMuseumData(this.searchTerm, 'met' , 1, 20).subscribe(res => {
        res['name'] = 'MET Museum';
        //const data = {'name': 'MET Museum', 'data': res};
        this.source.push(res);
        console.log(this.source);
      });
    }

    if (this.rijk) {
      // this.dataAccess.getRijksData(this.searchTerm, 0 , 20).subscribe(res => {
      this.dataAccess.getMuseumData(this.searchTerm, 'rijks' , 1, 20).subscribe(res => {
        // const data = {'name': 'Rijk Museum', 'data': res};
        res['name'] = 'Rijks Museum';
        this.source.push(res);
        console.log(this.source);
      });
    }

    if (this.cleveland) {
      // this.dataAccess.getClevelandData(this.searchTerm, 0 , 20).subscribe(res => {
      this.dataAccess.getMuseumData(this.searchTerm, 'cleveland' , 1, 20).subscribe(res => {
        // const data = {'name': 'Cleveland Museum', 'data': res};
        res['name'] = 'Cleveland Museum';
        this.source.push(res);
        console.log(this.source);
      });
    }

    if (this.local) {
      // this.dataAccess.getClevelandData(this.searchTerm, 0 , 20).subscribe(res => {
      this.dataAccess.getMuseumData(this.searchTerm, 'local' , 1, 20).subscribe(res => {
        // const data = {'name': 'Local Assets', 'data': res};
        res['name'] = 'Local';
        this.source.push(res);
        console.log(this.source);
      });
    }


  }
}
