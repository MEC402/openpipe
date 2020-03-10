import {Component, HostListener, Inject, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {NB_WINDOW, NbContextMenuDirective, NbDialogRef, NbDialogService, NbMenuService} from '@nebular/theme';

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

  constructor(private dataAccess: DataAccessService, private nbMenuService: NbMenuService) {
    dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
    nbMenuService.onItemClick().subscribe(d => {
      console.log(d);
      if (d.item.title == 'Edit') {

      } else if (d.item.title == 'Delete') {
        if (window.confirm('Are you sure you want to delete?')) {
          const index = this.collections.findIndex(c => c.name === d.tag);
          this.collections.splice(index, 1);
        } else {
        }
      }
    });
  }

  items = [
    { title: 'Edit' },
    { title: 'Delete' },
  ];
  isSingleView: any;

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

