import {Component, Input, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {NbDialogRef, NbDialogService, NbPopoverDirective} from '@nebular/theme';
import {DataAccessService} from '../../../services/data-access.service';

@Component({
  selector: 'ngx-preview-card',
  templateUrl: './preview-card.component.html',
  styleUrls: ['./preview-card.component.scss'],
})
export class PreviewCardComponent implements OnInit {

  @Input() asset;
  constructor(private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>,
              private dataAccess: DataAccessService) { }

  ngOnInit() {
  }


  openDialog(dialog: TemplateRef<any>) {
    const data = [];
    Object.keys(this.asset.sourceData).forEach(s => {
      data.push([s, this.asset.sourceData[s]]);
    });
    this.dialogRef = this.dialogService.open(dialog, { context: data });
  }
}
