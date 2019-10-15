import { Component, OnInit } from '@angular/core';
import {SmartTableData} from '../../../@core/data/smart-table';
import {LocalDataSource} from 'ng2-smart-table';
import {DataAccessService} from '../../../services/data-access.service';

@Component({
  selector: 'ngx-canonical-meta-tags',
  templateUrl: './canonical-meta-tags.component.html',
  styleUrls: ['./canonical-meta-tags.component.scss'],
})
export class CanonicalMetaTagsComponent {

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
      confirmSave : true,
    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
    columns: {
      name: {
        title: 'Tag Name',
        type: 'string',
      },
    },
  };

  source: LocalDataSource = new LocalDataSource();

  constructor(private dataAccess: DataAccessService) {
    dataAccess.getCanonicalMetaTags().subscribe(res => {
      this.source.load(res);
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
    console.log("edit");
    this.dataAccess.updateCanonicalMetaTag(event.data.id, event.newData.name);
    event.confirm.resolve();
  }

  onCreateConfirm(event) {
    console.log("create");
    console.log(event);
    this.dataAccess.addCanonicalMetaTag(event.newData.name);
    event.confirm.resolve();
  }
}
