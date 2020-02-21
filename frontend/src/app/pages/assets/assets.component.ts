import { Component, OnInit } from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';

@Component({
  selector: 'ngx-assets',
  templateUrl: './assets.component.html',
  styleUrls: ['./assets.component.scss'],
})
export class AssetsComponent implements OnInit {
  assets: any;

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
}
