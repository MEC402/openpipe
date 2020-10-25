import {Component, EventEmitter, Input, OnInit, Output, TemplateRef} from '@angular/core';
import {DataAccessService} from '../../../services/data-access.service';
import {NbDialogRef, NbDialogService, NbMenuService} from '@nebular/theme';
import {TopicDropDownComponent} from '../topic-drop-down/topic-drop-down.component';
import {LocalDataSource} from 'ng2-smart-table';
import {log} from 'util';

@Component({
  selector: 'ngx-folder-card',
  templateUrl: './folder-card.component.html',
  styleUrls: ['./folder-card.component.scss'],
})
export class FolderCardComponent implements OnInit {
  @Input() collection;
  @Output() folderOpen = new EventEmitter();
  @Output() folderDelete = new EventEmitter();
  newName: any;
  newImage: any;
  newVerified: any;

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


  constructor(private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>,
              private dataAccess: DataAccessService) { }

  ngOnInit() {
    const temp = [];
    for (const [key, value] of Object.entries(this.collection.metaTags)) {
      if (key != 'id' && key != 'metaDataId')
        temp.push({'tagName': key, 'value': value});
    }
    this.source.load(temp);
    this.newName = this.collection.name[0];
    this.newImage = this.collection.image[0];
    this.newVerified = !!this.collection.verified[0];
  }

  onFolderOpenClick() {
    this.folderOpen.emit();
  }

  onFolderEditClick(dialog: TemplateRef<any>) {
    this.newName = this.collection.name[0];
    this.newImage = this.collection.image[0];
    this.newVerified = !!this.collection.verified[0];
    this.dialogRef = this.dialogService.open(dialog, { context: 'data' });
  }

  onFolderDeleteClick() {
    this.dataAccess.deleteFolder(this.collection.id[0]);
    this.folderDelete.emit(this.collection);
  }

  saveFolderChanges() {
    this.dataAccess.updateFolder(this.collection.id[0], this.newName, this.newImage,this.newVerified).subscribe(res => {
    });
  }

  onDeleteConfirm(event): void {
    if (window.confirm('Are you sure you want to delete?')) {
      this.dataAccess.deleteMetaTag(this.collection.metaDataId[0], event.data.tagName, event.data.value[0])
        .subscribe(res => {
        });
      event.confirm.resolve();
    } else {
      event.confirm.reject();
    }
  }

  onEditConfirm(event) {
    this.dataAccess.updateMetaTag(this.collection.metaDataId[0], event.data.tagName,
      event.data.value[0], event.newData.tagName, event.newData.value).subscribe(res => {
      event.confirm.resolve();
    });
  }

  onCreateConfirm(event) {
    this.dataAccess.insertMetaTag(this.collection.metaDataId[0], event.newData.tagName, event.newData.value)
      .subscribe(res => {
      });
    event.confirm.resolve();
  }
}
