import { Component, OnInit } from '@angular/core';
import {DataAccessService} from "../../../services/data-access.service";
import {takeUntil} from "rxjs/operators";

@Component({
  selector: 'ngx-move-assets',
  templateUrl: './move-assets.component.html',
  styleUrls: ['./move-assets.component.scss']
})
export class MoveAssetsComponent implements OnInit {
  sourceFolder: any;
  collections: any;
  destFolder: any;

  sourceAssets = [];
  destAssets = [];

  pageSize = 10;
  totalSourcePages: number;
  sourceAssetsPage = 1;
  destAssetsPage = 1;
  totalDestPages;

  movedAssets=[];

  constructor(private dataAccess: DataAccessService) { }

  ngOnInit() {
    this.dataAccess.getFolders(1, 200).subscribe(res => {
      this.collections = res.data;
    });
  }

  onSourceSelect() {
    this.sourceAssets = [];
    this.totalSourcePages = Math.ceil(this.sourceFolder.assetCount / this.pageSize);
    this.dataAccess.getFolderAssets(this.sourceFolder.id, 1, this.pageSize).subscribe(res => {
      this.sourceAssets = this.sourceAssets.concat(res.data);
      console.log(this.sourceAssets);
    });
  }

  onDestSelect() {
    this.destAssets = [];

  }

  moveAssetToDestFolder(t: any) {
    console.log(t);
    this.destAssets.push(t);
  }

  prevSourceAssetsPage() {
    this.sourceAssetsPage--;
    this.dataAccess.getFolderAssets(this.sourceFolder.id, this.sourceAssetsPage, this.pageSize).subscribe(res => {
      this.sourceAssets = res.data;
    });
  }

  nextSourceAssetsPage() {
    this.sourceAssetsPage++;
    this.dataAccess.getFolderAssets(this.sourceFolder.id, this.sourceAssetsPage, this.pageSize).subscribe(res => {
      this.sourceAssets = res.data;

    });
  }

  saveChanges() {
    let saveData = {
      'folderId': this.destFolder.id,
      'assets': [],
    };
    this.destAssets.forEach(d => {
      saveData.assets.push(d.assetId);
    });
    console.log(saveData);
    this.dataAccess.addAssetsToFolder(saveData).subscribe(res => {
      this.destAssets = [];
      console.log(res);
    });
  }
}
