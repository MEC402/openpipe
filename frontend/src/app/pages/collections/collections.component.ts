import {Component, OnInit, TemplateRef} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {NbDialogRef, NbDialogService} from '@nebular/theme';

@Component({
  selector: 'ngx-collections',
  templateUrl: './collections.component.html',
  styleUrls: ['./collections.component.scss']
})
export class CollectionsComponent {
  collections: any;

  constructor(private dataAccess: DataAccessService,
              private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>) {
    dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
  }

  openDialog(dialog: TemplateRef<any>, collectionId) {
    this.dataAccess.getPublicAssetsInCollection(collectionId).subscribe(res => {
      this.dialogRef = this.dialogService.open(dialog, { context: res });
    });
  }
}
