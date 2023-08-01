import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {takeUntil} from 'rxjs/operators';
import {Observable, Subject} from 'rxjs';
import {DataAccessService} from '../../../services/data-access.service';
import {LocalDataSource} from 'ng2-smart-table';
import {AssetTagCardComponent} from '../../asset/asset-tag-card/asset-tag-card.component';

@Component({
  selector: 'ngx-folder-content',
  templateUrl: './folder-content.component.html',
  styleUrls: ['./folder-content.component.scss'],
})
export class FolderContentComponent implements OnInit, OnDestroy {

  @ViewChild(AssetTagCardComponent, { static: false }) assetTagInfo: AssetTagCardComponent;


  private folderId: string;
  folderInfo;
  currentFolderAssets: LocalDataSource = new LocalDataSource();
  items = [
    {title: 'Edit'},
    {title: 'Delete'},
  ];

  currentAsset: any;
  currentAssetType: string;
  currentAssetFullImage;
  currentAssetImage: any;
  showImage = false;
  loading: boolean;


  assetsSettings = {
    actions: {
      add: false,
      edit: false,
      delete: true,
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
          return '<img width="50px" src="' + openpipe_canonical_smallImage[0][Object.keys(openpipe_canonical_smallImage[0])[0]] + '" />';
        },
      },
      openpipe_canonical_title: {
        filter: true,
        title: 'Picture',
        type: 'html',
        valuePrepareFunction: (openpipe_canonical_title) => {
          return '<p>'+ openpipe_canonical_title[0][Object.keys(openpipe_canonical_title[0])[0]] + '</p>';
        },
      },
    },
  };

  constructor(private route: ActivatedRoute, private dataAccess: DataAccessService ) { }

  private _destroyed$ = new Subject();

  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }


  ngOnInit() {
    this.folderId = this.route.snapshot.paramMap.get('fid');

    const pageSize = 50;
    const pages = [];

    this.dataAccess.getFolderDetails(this.folderId).subscribe(r => {
      this.folderInfo = r;
    });


    this.dataAccess.getFolderAssets(this.folderId, 1, pageSize).pipe(takeUntil(this._destroyed$)).subscribe(res => {
      for (let i = 2; i <= Math.ceil(res.total / pageSize) ; i += 1) {
        pages.push(i);
      }
      this.currentFolderAssets.load(res.data);

      Observable.merge(pages.map( g => this.dataAccess.getFolderAssets(this.folderId, g, pageSize)))
        .subscribe(ob => {
          ob.pipe(takeUntil(this._destroyed$)).subscribe(resp => {
            resp.data.forEach(d => {
              this.currentFolderAssets.add(d).then(p => this.currentFolderAssets.refresh());
            });
          });
        });
    });
  }

  onFolderMemberDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      console.log(event);

      this.dataAccess.deleteAssetFromFolder(event.data.assetId, this.folderId).subscribe(res => {
        console.log(res);
      });
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }


  onClick(event) {
    console.log(this.currentFolderAssets)
    this.currentAsset = event.data;
    this.assetTagInfo.updateUI(this.currentAsset);
    this.currentAssetType = this.currentAsset.assetType;
    this.currentAssetImage = this.currentAsset.openpipe_canonical_smallImage[0][Object.keys(this.currentAsset.openpipe_canonical_smallImage[0])[0]]
    this.currentAssetFullImage = this.currentAsset.openpipe_canonical_fullImage[0][Object.keys(this.currentAsset.openpipe_canonical_fullImage[0])[0]]
    this.onFlipCard();
  }

  onFlipCard() {
    this.showImage = !this.showImage;
  }

}
