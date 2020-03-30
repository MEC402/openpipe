import {Component, HostListener, OnInit} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {LocalDataSource} from 'ng2-smart-table';

@Component({
  selector: 'ngx-assets',
  templateUrl: './assets.component.html',
  styleUrls: ['./assets.component.scss'],
})
export class AssetsComponent implements OnInit {
  searchTerm: string;
  currentAssets: LocalDataSource = new LocalDataSource();
  assets: any;
  page= 1;
  total;
  pageSize= 10;
  constructor(private dataAccess: DataAccessService) {

  }

  ngOnInit() {
    this.dataAccess.getAssetsWithGUID().subscribe(res => {
      for (let i = 1; i < res.total; i += 10) {
        this.dataAccess.getAllAssets(i,10).subscribe(resp => {
          resp.data.forEach(d => {
            this.currentAssets.add(d);
            this.currentAssets.refresh();
          });
        });
      }
    });
  }

  @HostListener('body:click', ['$event'])
  onMouseclick(event: any) {

    if ( (event.target && event.target.attributes.class &&
      event.target.attributes['class'].value.includes('ng2-smart-page'))) {
      console.log(event.target.innerText);
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
        console.log('hi is search');
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
