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

  private _destroyed$ = new Subject();
  constructor(private dataAccess: DataAccessService) {

  }

  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }

  ngOnInit() {
    for (let i = 1; i < 100; i += 1) {
      this.currentAssets.add(1);
    }
    for (let i = 1; i < 5000; i += 1) {
      this.dataAccess.getAllAssets(i, 1).pipe(takeUntil(this._destroyed$)).subscribe(resp => {
        resp.data.forEach(d => {
          this.currentAssets.prepend(d);
          this.currentAssets.refresh();
        });
      });
    }
    // this.dataAccess.getAssetsWithGUID().pipe(takeUntil(this._destroyed$)).subscribe(res => {
    //   Observable
    //     .merge(res.data.slice(0, 100).map( g => this.dataAccess.getGUID(g)))
    //     .subscribe(ob => {
    //       ob.pipe(takeUntil(this._destroyed$)).subscribe(resp => {
    //         this.currentAssets.add(resp.data[0]).then(p => this.currentAssets.refresh());
    //       });
    //     });
    // });
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
