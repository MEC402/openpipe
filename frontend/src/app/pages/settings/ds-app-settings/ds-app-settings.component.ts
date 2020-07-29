import { Component, OnInit } from '@angular/core';
import {DataAccessService} from "../../../services/data-access.service";
import {LocalDataSource} from "ng2-smart-table";

@Component({
  selector: 'ngx-ds-app-settings',
  templateUrl: './ds-app-settings.component.html',
  styleUrls: ['./ds-app-settings.component.scss']
})
export class DsAppSettingsComponent implements OnInit {
  source: LocalDataSource = new LocalDataSource();

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
      groupName: {
        title: 'Group Name',
        type: 'string',
      },
      key: {
        title: 'Key',
        type: 'string',
      },
      value: {
        title: 'Value',
        type: 'string',
      },
    },
  };

  constructor(private dataAccess: DataAccessService) { }

  ngOnInit() {
    this.dataAccess.getWallAppSettings().subscribe(res => {
      this.source.load(res.data);
    });
  }

  onEditConfirm(event: any) {
    let data = event.source.data;
    console.log(event)
    data = this.arrayRemove(data, event.data)
    data.push(event.newData)
    const sendData = {'total': data.length, data};
    console.log(sendData);
    this.dataAccess.setWallAppSettings(sendData).subscribe(res => {
      console.log(res);
    });
    event.confirm.resolve();
  }

  onDeleteConfirm(event: any) {
    let data = event.source.data;
    data = this.arrayRemove(data, event.data)
    const sendData = {'total': data.length, data};
    console.log(sendData);
    this.dataAccess.setWallAppSettings(sendData).subscribe(res => {
      console.log(res);
    });
    event.confirm.resolve();
  }

  onCreateConfirm(event: any) {
    let data = event.source.data;
    console.log(event)
    data = this.arrayRemove(data, event.newData)
    data.push(event.newData)
    const sendData = {'total': data.length, data};
    console.log(sendData);
    this.dataAccess.setWallAppSettings(sendData).subscribe(res => {
      console.log(res);
    });
    event.confirm.resolve();
  }

  arrayRemove(arr, value) {
  return arr.filter(function (ele) {
    return ele != value;
  });
}
}
