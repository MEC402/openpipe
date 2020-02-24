import { Component, OnInit } from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';

@Component({
  selector: 'ngx-assets',
  templateUrl: './assets.component.html',
  styleUrls: ['./assets.component.scss'],
})
export class AssetsComponent implements OnInit {
  assets: any;
  page=1;
  total;
  pageSize=10;
  constructor(private dataAccess: DataAccessService) {
    this.dataAccess.getAllAssets().subscribe(res => {
      console.log(res);
      this.assets = res;
    });
  }

  ngOnInit() {
  }

  onClick(asset: any) {
    if (asset.largeImage) {
      window.open(asset.largeImage, '_blank');
    }

  }

  nextPage() {
    // this.dataAccess.getMuseumData(this.searchTerm, source.sourceName , source.page + 1, source.pageSize)
    //   .subscribe(res => {
    //     console.log(res);
    //     source.data = res['data'];
    //     source.page = source.page + 1;
    //   });
  }

  prevPage() {
    // console.log(source);
    // this.dataAccess.getMuseumData(this.searchTerm, source.sourceName , source.page - 1, source.pageSize)
    //   .subscribe(res => {
    //     console.log(res);
    //     source.data = res['data'];
    //     source.page = source.page - 1;
    //   });
  }

  ceil(number: number) {
    // return Math.ceil(number);
  }
}
