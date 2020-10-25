import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {LocalDataSource, ViewCell} from "ng2-smart-table";
import {DataAccessService} from '../../../services/data-access.service';
import {ButtonViewComponent} from "../../home/home.component";
import {scanForRouteEntryPoints} from "@angular/compiler-cli/src/ngtsc/routing/src/lazy";




@Component({
  selector: 'ngx-asset-defects-report',
  templateUrl: './asset-defects-report.component.html',
  styleUrls: ['./asset-defects-report.component.scss']
})
export class AssetDefectsReportComponent implements OnInit {
   currentAsset=[];


  ngOnInit() {
  }

  settings = {
    pager: {
      display: true,
      perPage: 100,
    },
    actions: {
      add: false,
      delete: false,
      edit:false,
    },
    columns: {
      name: {
        title: 'Asset Name',
        type: 'string',
        editable: false,
      },
      Note: {
        title: 'Defect Type',
        type: 'string',
        editable: false,
      },
    },
  };


  tagSettings = {
    pager: {
      display: true,
      perPage: 100,
    },
    actions: {
      add: false,
      delete: false,
      edit:false,
    },
    columns: {
      tagName: {
        title: 'Tag Name',
        type: 'string',
        editable: false,
      },
      value: {
        title: 'Tag Value',
        type: 'string',
        editable: false,
      },
      note: {
        title: 'note',
        type: 'string',
      },
      verified: {
        title: 'Verified',
        type: 'custom',
        renderComponent: ButtonViewComponent,
        onComponentInitFunction(instance) {
          instance.save.subscribe(row => {
            row.verified=1;
          });
        },
      }
    },
  };

  map={};
  source: LocalDataSource = new LocalDataSource();
  tagSource: LocalDataSource = new LocalDataSource();
  loading=true;
  currentAssetName: any;

  constructor(private dataAccess: DataAccessService) {
    dataAccess.getAssetsReport(47).subscribe(res => {
      console.log(res)
      this.source.load(res.data);
      res.data.forEach(d => {
        console.log(d);
      });
      this.loading=false;

    });
  }


  onEditConfirm(event) {
    console.log('edit');
    this.dataAccess.updateCanonicalMetaTag(event.data.id, event.newData.name);
    event.confirm.resolve();
  }

  onClick(event) {
    this.currentAsset = event.data;
    // this.currentAssetName = this.currentAsset.name;
    // const temp = [];
    // for (const [key, value] of Object.entries(event.data)) {
    //   if (key != 'id' && key != 'metaDataId')
    //     temp.push({'tagName': key, 'value': value});
    // }
    // this.tagSource.load(this.currentAsset.tags);
  }


  Verify(d: any) {
    console.log(d);
  }

  VerifyAll() {

  }
}
