import { Component, OnInit } from '@angular/core';
import {DataAccessService} from '../../../services/data-access.service';
import {LocalDataSource} from "ng2-smart-table";

@Component({
  selector: 'ngx-meta-tag-editor',
  templateUrl: './meta-tag-editor.component.html',
  styleUrls: ['./meta-tag-editor.component.scss'],
})
export class MetaTagEditorComponent implements OnInit {
  collections: any;
  assets: any;
  settings = {
    add: {
      addButtonContent: '<i class="nb-plus"></i>',
      createButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmCreate: true,
    },
    edit: {
      editButtonContent: '<i class="nb-edit"></i>',
      saveButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmSave : true,
    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
    columns: {
      tagName: {
        title: 'Tag Name',
        type: 'string',
      },
      value: {
        title: 'Value',
        type: 'string',
      },
    },
  };

  source: LocalDataSource = new LocalDataSource();
  currentAsset: any;
  constructor(private dataAccess: DataAccessService) {
    this.dataAccess.getAllAssets().subscribe(res => {
      this.assets = res;
    });
  }

  ngOnInit() {
    // this.dataAccess.getPublicAssetsInCollection(collectionId).subscribe(res => {
    //
    // });
  }

  // onCollapseChange(event: boolean, c: any) {
  //   this.assets=[];
  //   if (!event) {
  //
  //   }
  // }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {

      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }

  onEditConfirm(event) {

    event.confirm.resolve();
  }

  onCreateConfirm(event) {

    event.confirm.resolve();
  }

  onClick(asset: any) {
    this.currentAsset = asset.name[0];
    this.dataAccess.getAssetMetaTags(asset.id[0]).subscribe(res => {

      let topics = [];
      res.data.forEach(metaTag => {
          topics.push({'id': metaTag['id'][0], 'assetId':metaTag['assetId'][0] ,'tagName': metaTag['tagName'][0], 'value': metaTag['value'][0]});
      });
      this.source.load(topics);
    });

  }
}
