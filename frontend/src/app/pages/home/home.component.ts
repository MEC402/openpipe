import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {LocalDataSource, ViewCell} from 'ng2-smart-table';

@Component({
  selector: 'button-view',
  template: `
    <button nbButton size="tiny" (click)="onClick()">Add to Folder</button>
  `,
})
export class ButtonViewComponent implements ViewCell, OnInit {
  renderValue: string;

  @Input() value: string | number;
  @Input() rowData: any;

  @Output() save: EventEmitter<any> = new EventEmitter();

  ngOnInit() {
    this.renderValue = this.value.toString().toUpperCase();
  }

  onClick() {
    this.save.emit(this.rowData);
  }
}

@Component({
  selector: 'ngx-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  searchTerm: string;
  source = [];
  met = true;
  rijk = true;
  cleveland = true;
  local = true;
  isSingleView = false;

  tableSource: LocalDataSource = new LocalDataSource();

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
      name: {
        title: 'Title',
        type: 'string',
      },
      button: {
        title: 'Button',
        type: 'custom',
        renderComponent: ButtonViewComponent,
        onComponentInitFunction(instance) {
          instance.save.subscribe(row => {

          });
        },
      },
    },
  };

  constructor(private dataAccess: DataAccessService) {
  }

  ngOnInit() {

  }

  searchAssets() {
    this.source = [];
    this.tableSource.empty();
    if (this.met) {
      // this.dataAccess.getMETsData(this.searchTerm, 0 , 20).subscribe(res => {
      this.dataAccess.getMuseumData(this.searchTerm, 'met' , 1, 20).subscribe(res => {
        res['name'] = 'MET Museum';
        res['sourceName'] = 'MET';
        res['page'] = 1;
        res['pageSize'] = 20;
        res['total'] = res['museumCount']['MET'];
        this.source.push(res);
        res['data'].forEach(d => {
          console.log(d);
          d['name'] = 'MET Museum';
          this.tableSource.add(d);
        });
        this.tableSource.refresh();
      });
    }

    if (this.rijk) {
      // this.dataAccess.getRijksData(this.searchTerm, 0 , 20).subscribe(res => {
      this.dataAccess.getMuseumData(this.searchTerm, 'rijks' , 1, 20).subscribe(res => {
        // const data = {'name': 'Rijk Museum', 'data': res};
        res['name'] = 'Rijks Museum';
        res['sourceName'] = 'Rijks';
        res['page'] = 1;
        res['pageSize'] = 20;
        res['total'] = res['museumCount']['Rijks'];
        this.source.push(res);
        res['data'].forEach(d => {
          console.log(d);
          d['name'] = 'Rijks Museum';
          this.tableSource.add(d);
        });
        this.tableSource.refresh();
      });
    }

    if (this.cleveland) {
      // this.dataAccess.getClevelandData(this.searchTerm, 0 , 20).subscribe(res => {
      this.dataAccess.getMuseumData(this.searchTerm, 'Cleveland' , 1, 20).subscribe(res => {
        // const data = {'name': 'Cleveland Museum', 'data': res};
        res['name'] = 'Cleveland Museum';
        res['sourceName'] = 'Cleveland';
        res['page'] = 1;
        res['pageSize'] = 20;
        res['total'] = res['museumCount']['Cleveland'];
        this.source.push(res);
        res['data'].forEach(d => {
          console.log(d);
          d['name'] = 'Cleveland Museum';
          this.tableSource.add(d);
        });
        this.tableSource.refresh();
      });
    }

    if (this.local) {
      // this.dataAccess.getClevelandData(this.searchTerm, 0 , 20).subscribe(res => {
      this.dataAccess.getMuseumData(this.searchTerm, 'local' , 1, 20).subscribe(res => {
        // const data = {'name': 'Local Assets', 'data': res};
        res['name'] = 'Local';
        res['page'] = 1;
        res['pageSize'] = 20;
        this.source['data'].push(res);
        res['data'].forEach(d => {
          console.log(d);
          d['name'] = 'Local';
          this.tableSource.add(d);
        });
        this.tableSource.refresh();
      });
    }

  }

  nextPage(source) {
    this.dataAccess.getMuseumData(this.searchTerm, source.sourceName , source.page + 1, source.pageSize)
      .subscribe(res => {
      source.data = res['data'];
      source.page = source.page + 1;
    });

  }

  prevPage(source) {

    this.dataAccess.getMuseumData(this.searchTerm, source.sourceName , source.page - 1, source.pageSize)
      .subscribe(res => {
        source.data = res['data'];
        source.page = source.page - 1;
      });

  }

  ceil(number: number) {
    return Math.ceil(number);
  }
}
