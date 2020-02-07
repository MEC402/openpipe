import { Component, OnInit } from '@angular/core';
import {LocalDataSource} from 'ng2-smart-table';
import {DataAccessService} from '../../../services/data-access.service';

@Component({
  selector: 'ngx-missing-images',
  templateUrl: './missing-images.component.html',
  styleUrls: ['./missing-images.component.scss'],
})
export class MissingImagesComponent implements OnInit {

  ngOnInit() {
  }

  settings = {
    actions: {
      add: false,
      delete: false,
    },
    edit: {
      editButtonContent: '<i class="nb-edit"></i>',
      saveButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmSave : true,
    },
    columns: {
      name: {
        title: 'Asset',
        type: 'string',
        editable: false,
      },
      value: {
        title: 'Tag Default Value',
        type: 'string',
      },
    },
  };

  source: LocalDataSource = new LocalDataSource();

  constructor(private dataAccess: DataAccessService) {
    dataAccess.getCanonicalMetaTags().subscribe(res => {
      const canonicalData = [];
      Object.keys(res).forEach(key => {
        const elem = {};
        elem['name'] = key;
        elem['value'] = res[key][0];
        canonicalData.push(elem);
      });
      this.source.load(canonicalData);
    });
  }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      this.dataAccess.deleteCanonicalMetaTag(event.data.id);
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }

  onEditConfirm(event) {
    console.log('edit');
    this.dataAccess.updateCanonicalMetaTag(event.data.id, event.newData.name);
    event.confirm.resolve();
  }

  onCreateConfirm(event) {
    console.log('create');
    console.log(event);
    this.dataAccess.addCanonicalMetaTag(event.newData.name);
    event.confirm.resolve();
  }

}
