import {Component, HostListener, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {NbContextMenuDirective, NbDialogRef, NbDialogService} from '@nebular/theme';

@Component({
  selector: 'ngx-collections',
  templateUrl: './collections.component.html',
  styleUrls: ['./collections.component.scss'],
})
export class CollectionsComponent {
  @ViewChild(NbContextMenuDirective, { static: false }) contextMenu: NbContextMenuDirective;

  collections: any;
  assets: any;
  currentFolder: any;
  metaTags: any;

  constructor(private dataAccess: DataAccessService) {
    dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
  }

  items = [
    { title: 'Edit' },
    { title: 'Delete' },
  ];

  open() {
    this.contextMenu.show();
    return false;
  }

  @HostListener('document:click')
  close() {
    this.contextMenu.hide();
  }



  onClick(element) {
    this.currentFolder = element.name;
    this.dataAccess.getPublicAssetsInCollection(element.id).subscribe(res => {
      this.assets = res.data;
      console.log(this.assets);
    });
  }

  metaShow(event) {
    console.log(event);
    this.metaTags = event.data;
  }

  backToFolders() {
    this.assets = [];
  }
}

