import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {LocalDataSource, ViewCell} from 'ng2-smart-table';

@Component({
  selector: 'button-view',
  template: `<button nbButton size="tiny" (click)="onClick()">{{renderValue}}</button>`,
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
  sourceCheckboxes = [{name: 'Local', checked: false}];
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
    this.dataAccess.getMuseumInfo().subscribe(res => {
      res.museum1.forEach(d => {
        this.sourceCheckboxes.push({name: d.source, checked: false});
      });
    });

  }

  searchAssets() {
    this.source = [];
    this.tableSource.empty();

    this.sourceCheckboxes.forEach(museumSource => {
      if (museumSource.checked) {
          this.dataAccess.getMuseumData(this.searchTerm, museumSource.name, 1, 20).subscribe(res => {
            res['name'] = museumSource.name;
            res['sourceName'] = museumSource.name;
            res['page'] = 1;
            res['pageSize'] = 20;
            res['total'] = res['museumCount'][museumSource.name];
            this.source.push(res);
            res['data'].forEach(d => {
              // console.log(d);
              d['name'] = museumSource.name;
              this.tableSource.add(d);
            });
            this.tableSource.refresh();
          });
      }
    });
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
