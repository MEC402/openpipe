import {Component, Input, OnInit} from '@angular/core';
import {DataAccessService} from '../../../services/data-access.service';
import {LocalDataSource} from 'ng2-smart-table';

@Component({
  selector: 'ngx-meta-tag-editor',
  templateUrl: './meta-tag-editor.component.html',
  styleUrls: ['./meta-tag-editor.component.scss'],
})
export class MetaTagEditorComponent implements OnInit {
  @Input() assetsSource;
  collections: any;
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
      confirmSave: true,
      mode : 'inline',
    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
    columns: {
      tagName: {
        title: 'Tag Name',
        type: 'string',
      },
      value: {
        title: 'Value',
        type: 'string',
      },
    },
  };


  source: LocalDataSource = new LocalDataSource();
  currentAsset: any;
  currentAssetName: any;



  assetsSettings = {
    actions: false,
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
    },
  };

// <button nbSuffix nbButton ghost (click)="toggleShowPassword()">
// <nb-icon [icon]="showPassword ? 'eye-outline' : 'eye-off-2-outline'"
//   pack="eva"
//     [attr.aria-label]="showPassword ? 'hide password' : 'show password'">
//     </nb-icon>
//     </button>

  constructor(private dataAccess: DataAccessService) {
    // this.dataAccess.getAllAssets().subscribe(res => {
    //   console.log(res);
    //   this.assetsSource.load(res.data);
    //   this.assets = res;
    // });
  }

  ngOnInit() {

  }

  onDeleteConfirm(event): void {
    console.log('delete');
    console.log(event);
    if (window.confirm('Are you sure you want to delete?')) {
      this.dataAccess.deleteMetaTag(this.currentAsset.metaDataId, event.data.tagName, event.data.value[0]).subscribe(res => {
        console.log(res);
      });
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }

  onEditConfirm(event) {
    console.log('edit');
    console.log(event);
    this.dataAccess.updateMetaTag(this.currentAsset.metaDataId,event.data.tagName,event.data.value,event.newData.tagName,event.newData.value)
      .subscribe(res => {
        console.log(res);
        event.confirm.resolve();
      });
  }

  onCreateConfirm(event) {
    console.log('add');
    console.log(event);
    this.dataAccess.insertMetaTag(this.currentAsset.metaDataId, event.newData.tagName, event.newData.value).subscribe(res => {
      console.log(res);
    });
    event.confirm.resolve();
  }

  onClick(event) {
    this.currentAsset = event.data;
    this.currentAssetName=this.currentAsset.openpipe_canonical_title[0]
    let temp = [];
    console.log(event);
    for (const [key, value] of Object.entries(event.data)) {
      if (key != 'id' && key!='metaDataId')
        temp.push({'tagName': key, 'value': value});
    }
    this.source.load(temp);
  }
}
