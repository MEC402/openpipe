import {Component, EventEmitter, Input, OnInit, Output, TemplateRef, ViewChild} from '@angular/core';
import {NbDialogRef, NbDialogService, NbPopoverDirective} from '@nebular/theme';
import {DataAccessService} from '../../../services/data-access.service';

@Component({
  selector: 'ngx-preview-card',
  templateUrl: './preview-card.component.html',
  styleUrls: ['./preview-card.component.scss'],
})
export class PreviewCardComponent implements OnInit {
  assetElem: any;
  assets: any;
  @Output() valueChange = new EventEmitter();
  @Input() asset;

  constructor(private dataAccess: DataAccessService) { }

  ngOnInit() {
  }


  showMeta(assetElem) {
    this.dataAccess.getAssetMetaTags(assetElem.id).subscribe(res => {
      this.valueChange.emit(res);
    });
  }
}
