import {Component, OnInit, TemplateRef} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {NbDialogRef, NbDialogService} from '@nebular/theme';

@Component({
  selector: 'ngx-collections',
  templateUrl: './collections.component.html',
  styleUrls: ['./collections.component.scss'],
})
export class CollectionsComponent {
  collections: any;
  assets: any;
  currentFolder: any;
  metaTags: any;

  constructor(private dataAccess: DataAccessService) {
    dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
  }



  onClick(element) {
    this.currentFolder = element.name;
    this.dataAccess.getPublicAssetsInCollection(element.id).subscribe(res => {
      this.assets = res.data;
    });
  }

  metaShow(event) {
    console.log(event);
    this.metaTags = event.data;
  }
}

