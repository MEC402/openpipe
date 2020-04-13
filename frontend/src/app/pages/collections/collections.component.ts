import {Component, OnInit, ViewChild} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {NbContextMenuDirective, NbPopoverDirective} from '@nebular/theme';
import {LocalDataSource} from 'ng2-smart-table';
import {Subject} from 'rxjs';

@Component({
  selector: 'ngx-collections',
  templateUrl: './collections.component.html',
  styleUrls: ['./collections.component.scss'],
})
export class CollectionsComponent implements OnInit {
  protected destroy$ = new Subject<void>();

  collections: any;
  assets= [];
  currentFolder = {'name': ['test'], 'id': [-1]};
  metaTags: any;
  newCollectionName;
  @ViewChild(NbPopoverDirective, { static: false }) popover: NbPopoverDirective;


  items = [
    {title: 'Edit'},
    {title: 'Delete'},
  ];

  isSingleView= true;
  currentFolderAssets: LocalDataSource = new LocalDataSource();
  source: LocalDataSource = new LocalDataSource();
  currentAsset: any;
  currentAssetName: any;

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
      confirmSave: true,
      mode : 'inline',
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

  assetsSettings = {
    actions: {
      add: false,
      edit: false,
    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
    columns: {
      openpipe_canonical_smallImage: {
        filter: false,
        title: 'Picture',
        type: 'html',
        valuePrepareFunction: (openpipe_canonical_smallImage) => {
          return '<img width="50px" src="' + openpipe_canonical_smallImage[0] + '" />';
        },
      },
      openpipe_canonical_title: {
        title: 'Title',
        type: 'string',
      },
    },
  };
  folderPage = true;

  constructor(private dataAccess: DataAccessService) {
    dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
  }

  ngOnInit() {

  }


  onFolderMemberDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      this.dataAccess.deleteFolderMember(this.currentFolder.id[0], event.data.id[0]);
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }

  onDeleteConfirm(event): void {

    if (window.confirm('Are you sure you want to delete?')) {
      this.dataAccess.deleteMetaTag(this.currentAsset.metaDataId, event.data.tagName, event.data.value[0])
        .subscribe(res => {
      });
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }

  onEditConfirm(event) {
    this.dataAccess.updateMetaTag(this.currentAsset.metaDataId, event.data.tagName, event.data.value,
      event.newData.tagName, event.newData.value)
      .subscribe(res => {
        event.confirm.resolve();
    });
  }

  onCreateConfirm(event) {
    this.dataAccess.insertMetaTag(this.currentAsset.metaDataId, event.newData.tagName, event.newData.value)
      .subscribe(res => {
    });
    event.confirm.resolve();
  }

  onClick(event) {
    this.currentAsset = event.data;
    this.currentAssetName = this.currentAsset.openpipe_canonical_title[0];
    const temp = [];
    for (const [key, value] of Object.entries(event.data)) {
      if (key != 'id' && key != 'metaDataId')
        temp.push({'tagName': key, 'value': value});
    }
    this.source.load(temp);
  }


  onFolderOpenClick(element) {
    this.folderPage = false;
    this.currentFolder = element;
    this.dataAccess.getGUID('http://mec402.boisestate.edu/cgi-bin/openpipe/data/folder/' +
      this.currentFolder.id[0]).subscribe(res => {
      for (let i = 1; i < (res.assets.length / 10) + 1; i += 1) {
        this.dataAccess.getPublicAssetsInCollection(element.id, i, 10).subscribe(resp => {
          // this.assets.concat(resp.data);
          resp.data.forEach(d => {
            this.assets.push(d);
            this.currentFolderAssets.add(d);
            this.currentFolderAssets.refresh();
          });
        });
      }
    });
  }

  metaShow(event) {
    this.metaTags = event.data;
  }

  backToFolders() {
    this.assets = [];
    this.currentFolderAssets.empty();
    this.source.empty();
    this.folderPage = true;
  }

  onFolderDeleteClick(c) {
    this.dataAccess.deleteFolder(c.id[0]);
    for ( let i = 0; i < this.collections.length; i++) {
      if ( this.collections[i].id[0] === c.id[0]) {
        this.collections.splice(i, 1);
        break;
      }
    }
  }

  onCreateCollection() {
    this.popover.hide();
    this.dataAccess.createCollection(this.newCollectionName).subscribe(res0 => {
      this.dataAccess.getCollections().subscribe(res => {
          this.collections = res.data;
      });
    });
  }

}

