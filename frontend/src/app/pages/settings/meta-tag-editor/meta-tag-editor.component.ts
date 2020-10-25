import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {DataAccessService} from '../../../services/data-access.service';
import {LocalDataSource} from 'ng2-smart-table';
import {TopicDropDownComponent} from '../../util/topic-drop-down/topic-drop-down.component';

@Component({
  selector: 'ngx-meta-tag-editor',
  templateUrl: './meta-tag-editor.component.html',
  styleUrls: ['./meta-tag-editor.component.scss'],
})
export class MetaTagEditorComponent implements OnInit {
  @Input() assetsSource;
  @Input() loading = false;
  @Input() value;

  @ViewChild('test', {static: false}) asdf;

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
        type: 'html',
        editor: {
          type: 'custom',
          valuePrepareFunction: (cell, row) => row,
          component: TopicDropDownComponent,
        },
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

  constructor(private dataAccess: DataAccessService) {

  }

  ngOnInit() {
  }

  onDeleteConfirm(event): void {
     if (window.confirm('Are you sure you want to delete?')) {
      this.dataAccess.deleteMetaTag(this.currentAsset.metaDataId, event.data.tagName, event.data.value[0])
        .subscribe(res => {
      });
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }

  onEditConfirm(event) {
    this.dataAccess.updateMetaTag(this.currentAsset.metaDataId, event.data.tagName,
      event.data.value, event.newData.tagName, event.newData.value).subscribe(res => {
        event.confirm.resolve();
      });
  }

  onCreateConfirm(event) {
    this.dataAccess.insertMetaTag(this.currentAsset.metaDataId, event.newData.tagName, event.newData.value)
      .subscribe(res => {
    });
    event.confirm.resolve();
  }

  onClick(event) {
    this.currentAsset = event.data;
    this.currentAssetName = this.currentAsset.openpipe_canonical_title[0];
    const temp = [];
    for (const [key, value] of Object.entries(event.data)) {
      if (key != 'id' && key != 'metaDataId')
        temp.push({'tagName': key, 'value': value});
    }
    this.source.load(temp);
  }
}
