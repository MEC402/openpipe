import { Component, OnInit } from '@angular/core';
import {LocalDataSource} from "ng2-smart-table";
import {DataAccessService} from '../../../services/data-access.service';

@Component({
  selector: 'ngx-asset-defects-report',
  templateUrl: './asset-defects-report.component.html',
  styleUrls: ['./asset-defects-report.component.scss']
})
export class AssetDefectsReportComponent implements OnInit {


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
      assetName: {
        title: 'Asset Name',
        type: 'string',
        editable: false,
      },
      defectType: {
        title: 'Defect Type',
        type: 'string',
        editable: false,
      },
      metaTagName: {
        title: 'MetaTag Name',
        type: 'string',
        editable: false,
      },
      metaTagValue: {
        title: 'MetaTag Value',
        type: 'string',
      },
      sourceName: {
        title: 'Source Museum',
        type: 'string',
        editable: false,
      },
    },
  };



  source: LocalDataSource = new LocalDataSource();

  constructor(private dataAccess: DataAccessService) {
    dataAccess.getAssetsReport().subscribe(res => {
      console.log(res)
      this.source.load(res.data);
    });
  }


  onEditConfirm(event) {
    console.log('edit');
    this.dataAccess.updateCanonicalMetaTag(event.data.id, event.newData.name);
    event.confirm.resolve();
  }


}
