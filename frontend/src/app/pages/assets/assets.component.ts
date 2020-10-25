import {Component, HostListener, OnDestroy, OnInit} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {LocalDataSource} from 'ng2-smart-table';
import {Observable, Subject} from 'rxjs';
import 'rxjs/add/operator/map';
import 'rxjs/add/observable/merge';
import {takeUntil} from 'rxjs/operators';

@Component({
  selector: 'ngx-assets',
  templateUrl: './assets.component.html',
  styleUrls: ['./assets.component.scss'],
})
export class AssetsComponent implements OnInit, OnDestroy {
  searchTerm: string;
  currentAssets: LocalDataSource = new LocalDataSource();
  assets: any;
  page = 1;
  total;
  pageSize = 10;
  pages = [2, 3, 4, 5, 6, 7, 8, 9, 10];
  private _destroyed$ = new Subject();
  loading = true;
  currentTopics: any;
  constructor(private dataAccess: DataAccessService) {
  }

  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }

  ngOnInit() {
    this.dataAccess.getCanonicalMetaTags().subscribe(d => {
      this.dataAccess.changeMessage(d);
    });

    // for (let i = 1; i < 5000; i += 1) {
    //   this.dataAccess.getAllAssets(i, 200).pipe(takeUntil(this._destroyed$)).subscribe(resp => {
    //     resp.data.forEach(d => {
    //       this.currentAssets.add(d);
    //       this.currentAssets.refresh();
    //     });
    //   });
    // }
    this.dataAccess.getAllAssets(1, 200).pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.loading = false;
      this.currentAssets.load(res.data);
      Observable.merge(this.pages.map( g => this.dataAccess.getAllAssets(g, 200)))
        .subscribe(ob => {
          ob.pipe(takeUntil(this._destroyed$)).subscribe(resp => {
            resp.data.forEach(d => {
              this.currentAssets.add(d).then(p => this.currentAssets.refresh());
            });
          });
        });
    });
  }

  // ngOnInit() {
  //   this.dataAccess.getAssetsWithGUID().subscribe(res => {
  //     res.data.slice(0, 100).map( g => this.dataAccess.getGUID(g)
  //       .subscribe(r => this.currentAssets.add(r.data[0]).then(rr => this.currentAssets.refresh())));
  //   });
  // }

  // ngOnInit() {
  //   this.dataAccess.getAllAssets(1,100).subscribe(res => {
  //     res.data.forEach(d => {
  //       console.log(d)
  //       this.currentAssets.add(d).then(r => this.currentAssets.refresh());
  //     });
  //   });
  // }

  @HostListener('body:click', ['$event'])
  onMouseclick(event: any) {
    if ( (event.target && event.target.attributes.class &&
      event.target.attributes['class'].value.includes('ng2-smart-page'))) {
    }
  }

  onClick(asset: any) {
    if (asset.largeImage) {
      window.open(asset.largeImage, '_blank');
    }
  }

  searchAssets() {
    this.dataAccess.getMuseumData(this.searchTerm, 'local' , 1, 20).subscribe(res => {
      this.currentAssets.load([]);

      this.assets = [];
      this.currentAssets.load(res.data);
      this.assets = res;
    });
  }

  nextPage() {
    // this.dataAccess.getMuseumData(this.searchTerm, source.sourceName , source.page + 1, source.pageSize)
    //   .subscribe(res => {
    //     console.log(res);
    //     source.data = res['data'];
    //     source.page = source.page + 1;
    //   });
  }

  prevPage() {
    // console.log(source);
    // this.dataAccess.getMuseumData(this.searchTerm, source.sourceName , source.page - 1, source.pageSize)
    //   .subscribe(res => {
    //     console.log(res);
    //     source.data = res['data'];
    //     source.page = source.page - 1;
    //   });
  }

  ceil(number: number) {
    // return Math.ceil(number);
  }


}
