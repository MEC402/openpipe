import {Component, ElementRef, HostListener, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {LocalDataSource} from 'ng2-smart-table';
import {DataAccessService} from '../../../services/data-access.service';
import {AssetTagCardComponent} from '../../asset/asset-tag-card/asset-tag-card.component';
import {ActivatedRoute} from '@angular/router';
import {Observable, Subject} from 'rxjs';
import {takeUntil} from 'rxjs/operators';
import {log} from 'util';

@Component({
  selector: 'ngx-asset-changes',
  templateUrl: './asset-changes.component.html',
  styleUrls: ['./asset-changes.component.scss'],
})
export class AssetChangesComponent implements OnInit, OnDestroy {
  @ViewChild(AssetTagCardComponent, { static: false }) assetTagInfo: AssetTagCardComponent;


  totalAssets = 0;
  folderInfo;
  changedAssets: LocalDataSource = new LocalDataSource();
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
      delete: false,
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
      lastModified: {
        title: 'modified Date',
        type: 'string',
      },
    },
  };

  constructor(private route: ActivatedRoute, private dataAccess: DataAccessService ) { }

  private _destroyed$ = new Subject();
  ngModelDate = new Date();

  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }


  ngOnInit() {
    this.onDateChange();
  }

  onDateChange() {
    this.changedAssets.empty();
    const formattedDate = this.ngModelDate.getFullYear() + '-' +
      (this.ngModelDate.getMonth() + 1) + '-' +
      this.ngModelDate.getDate();

    console.log(formattedDate);
    const pageSize = 50;
    const pages = [];

    this.dataAccess.getChangedAssets(formattedDate, 1, pageSize).pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalAssets = res.total;
      for (let i = 2; i <= Math.ceil(res.total / pageSize) ; i += 1) {
        pages.push(i);
      }
      this.changedAssets.load(res.data);
      Observable.merge(pages.map( g => this.dataAccess.getChangedAssets(formattedDate, g, pageSize)))
        .subscribe(ob => {
          ob.pipe(takeUntil(this._destroyed$)).subscribe(resp => {
            resp.data.forEach(d => {
              this.changedAssets.add(d).then(p => this.changedAssets.refresh());
            });
          });
        });
    });
  }

  onClick(event) {
    this.currentAsset = event.data;
    this.assetTagInfo.updateUI(this.currentAsset);
    this.currentAssetType = this.currentAsset.assetType;
    this.currentAssetImage = this.currentAsset.openpipe_canonical_smallImage[0];
    this.currentAssetFullImage = this.currentAsset.openpipe_canonical_fullImage[0];
    console.log(this.currentAsset);
    this.onFlipCard();
  }

  onFlipCard() {
    this.showImage = !this.showImage;
  }
}
