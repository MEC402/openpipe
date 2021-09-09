import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {NbContextMenuDirective, NbPopoverDirective} from '@nebular/theme';
import {LocalDataSource} from 'ng2-smart-table';
import {Observable, Subject} from 'rxjs';
import {takeUntil} from 'rxjs/operators';


@Component({
  selector: 'ngx-collections',
  templateUrl: './collections.component.html',
  styleUrls: ['./collections.component.scss'],
})
export class CollectionsComponent implements OnInit, OnDestroy {
  protected destroy$ = new Subject<void>();

  collections = [];
  assets = [];
  currentFolder = {'name': ['test'], 'id': [-1]};
  metaTags: any;
  newCollectionName;
  @ViewChild(NbPopoverDirective, { static: false }) popover: NbPopoverDirective;


  items = [
    {title: 'Edit'},
    {title: 'Delete'},
  ];

  isSingleView = true;
  currentFolderAssets: LocalDataSource = new LocalDataSource();
  source: LocalDataSource = new LocalDataSource();
  currentAsset: any;
  currentAssetName: any;
  currentAssetVerified = false;
  currentAssetLink: string;
  currentAssetScore: number;
  selectedAssetMetaTag = [];
  selectedAssetChanges = {};
  selectTagNames = ['openpipe_canonical_artist', 'openpipe_canonical_title',  'openpipe_canonical_displayDate' , 'openpipe_canonical_date',
    'openpipe_canonical_Moment', 'openpipe_canonical_medium', 'openpipe_canonical_Technique', 'openpipe_canonical_country'
    , 'openpipe_canonical_culture', 'openpipe_canonical_period', 'openpipe_canonical_biography'
    , 'openpipe_canonical_longitude', 'openpipe_canonical_latitude', 'openpipe_canonical_classification',
    'openpipe_canonical_Object_Type', 'openpipe_canonical_Region', 'openpipe_canonical_largeImageDimensions'];

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
      verified: {
        title: 'Verif',
        type: 'string',
      },
    },
  };

  assetsSettings = {
    actions: {
      add: false,
      edit: false,
      delete: false,
    },
    // delete: {
    //   deleteButtonContent: '<i class="nb-trash"></i>',
    //   confirmDelete: true,
    // },
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
  currentAssetImage: any;
  showImage = false;
  loading: boolean;

  constructor(private dataAccess: DataAccessService) {
    // this.db.collection('folders', ref => ref.orderBy('folderInfo.name')).get().subscribe(snap => {
    //   snap.forEach(snap => {
    //     this.collections.push(snap.data().folderInfo)
    //     console.log(snap.id);
    //     console.log(snap.data().folderInfo);
    //   });
    // });

    this.loading = true;
    dataAccess.getFolders(1, 200).subscribe(res => {
      this.loading = false;
      console.log(res.data);
      this.collections = res.data;
    });

  }

  private _destroyed$ = new Subject();
  assetLink: any;
  currentAssetAccessStatus = true;
  allTagsView = false;


  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }

  ngOnInit() {
    this.dataAccess.getCanonicalMetaTags().subscribe(d => {
      this.dataAccess.changeMessage(d);
    });

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
    console.log(this.currentAsset);
    this.currentAssetName = this.currentAsset.openpipe_canonical_title[0];
    this.currentAssetImage = this.currentAsset.openpipe_canonical_smallImage[0];
    this.currentAssetVerified = this.currentAsset.assetVerified[0];
    this.currentAssetScore = this.currentAsset.assetScore;
    this.currentAssetAccessStatus = true;
    this.selectedAssetChanges = {};
    const s = this.currentAsset.openpipe_canonical_source[0];

    if (s.includes('Metropolitan')) {
        this.currentAssetLink = 'https://www.metmuseum.org/art/collection/search/' + this.currentAsset.objectID;
    } else if (s.includes('Cleveland')) {
        this.currentAssetLink = 'https://www.clevelandart.org/art/' + this.currentAsset.accession_number;
    } else {
      this.currentAssetLink = 'Link not available';
    }

    console.log(event.data);
    const temp = [];
    for (const [key, value] of Object.entries(event.data)) {
      if (this.selectTagNames.includes(key))
        temp.push({'tagName': key.split('_')[2], 'value': value, 'originalTagName': key});
    }
    this.selectedAssetMetaTag = temp;
    this.source.load(temp);
    this.onFlipCard();
  }


  onFolderOpenClick(element) {
    this.folderPage = false;
    this.currentFolder = element;
    const pageSize = 50;
    let pages = [];

    for (let i = 2; i < Math.ceil(element.assetCount / pageSize) ; i += 1) {
      pages.push(i);
    }

    this.dataAccess.getFolderAssets(element.id, 1, pageSize).pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.loading = false;
      this.currentFolderAssets.load(res.data);
      Observable.merge(pages.map( g => this.dataAccess.getFolderAssets(element.id, g, pageSize)))
        .subscribe(ob => {
          ob.pipe(takeUntil(this._destroyed$)).subscribe(resp => {
            resp.data.forEach(d => {
              this.currentFolderAssets.add(d).then(p => this.currentFolderAssets.refresh());
            });
          });
        });
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
    this.currentAssetVerified = false;
    this.currentAssetName = '';
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

  onFlipCard() {
    this.showImage = !this.showImage;
  }

  showAllTags() {
    const temp = [];
    if (!this.allTagsView){
      this.allTagsView = true;
      for (const [key, value] of Object.entries(this.currentAsset)) {
        temp.push({'tagName': key, 'value': value, 'originalTagName': key});
      }
    } else {
      this.allTagsView = false;
      for (const [key, value] of Object.entries(this.currentAsset)) {
        if (this.selectTagNames.includes(key))
          temp.push({'tagName': key.split('_')[2], 'value': value, 'originalTagName': key});
      }
    }
    this.selectedAssetMetaTag = temp;
  }

  saveAssetChanges() {
    this.dataAccess.saveAssetChanges(this.currentAsset.metaDataId, this.selectedAssetChanges).subscribe(res => {
      console.log(res);
    });
  }

  sendTheNewValue(e) {
    this.selectedAssetChanges[e.target.id] = e.target.value;
  }
}

