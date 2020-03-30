import {Component, EventEmitter, Input, OnInit, Output, TemplateRef} from '@angular/core';
import {DataAccessService} from "../../../services/data-access.service";
import {NbDialogRef, NbDialogService, NbMenuService} from "@nebular/theme";

@Component({
  selector: 'ngx-folder-card',
  templateUrl: './folder-card.component.html',
  styleUrls: ['./folder-card.component.scss']
})
export class FolderCardComponent implements OnInit {
  @Input() collection;
  @Output() folderOpen= new EventEmitter();
  @Output() folderDelete= new EventEmitter();
  newName: any;
  newImage: any;


  constructor(private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>,
              private dataAccess: DataAccessService) { }

  ngOnInit() {
  }

  onFolderOpenClick() {
    this.folderOpen.emit();
  }

  onFolderEditClick(dialog: TemplateRef<any>) {
    this.newName = this.collection.name[0];
    this.newImage = this.collection.image[0];
    this.dialogRef = this.dialogService.open(dialog, { context: 'data' });
  }

  onFolderDeleteClick() {
    console.log('delete');
    this.dataAccess.deleteFolder(this.collection.id[0]);
    this.folderDelete.emit(this.collection);
  }

  saveFolderChanges() {
    this.dataAccess.updateFolder(this.collection.id[0],this.newName,this.newImage).subscribe(res => {
      console.log(res);
    });
  }
}
