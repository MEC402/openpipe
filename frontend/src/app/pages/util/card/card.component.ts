import {Component, Input, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {NbDialogRef, NbDialogService, NbPopoverDirective, NbWindowService} from '@nebular/theme';
import {DataAccessService} from '../../../services/data-access.service';

@Component({
  selector: 'ngx-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss'],
})
export class CardComponent implements OnInit {
  @Input() asset;
  @Input() source;
  @Input() searchTerm;
  chosenMetaData= {};
  collections= [];
  newCollectionName;
  chosenCollection;
  scope;
  @ViewChild('contentTemplate', { static: false }) contentTemplate: TemplateRef<any>;
  @ViewChild(NbPopoverDirective, { static: false }) popover: NbPopoverDirective;
  check = true;

  constructor(private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>,
              protected collectionDialogRef: NbDialogRef<any>,
              private dataAccess: DataAccessService) { }

  ngOnInit() {
  }

  getAssetsSourceMetaTags() {
    const data = [];
    Object.keys(this.asset).forEach(s => {
      data.push([s, this.asset[s]]);
    });
    return data;
  }

  openDialog(dialog: TemplateRef<any>) {
    const data = [];
    Object.keys(this.asset).forEach(s => {
      if (!s.includes('openpipe')) {
        data.push([s, JSON.stringify(this.asset[s]).replace(/['"]+/g, '')]);
        this.chosenMetaData[s] = JSON.stringify(this.asset[s]).replace(/['"]+/g, '');
      } else {
        data.push([s, JSON.stringify(this.asset[s][0]).replace(/['"]+/g, '')]);
        this.chosenMetaData[s] = JSON.stringify(this.asset[s][0]).replace(/['"]+/g, '');
      }
    });
    this.dataAccess.getCollections().subscribe(res => {
      console.log(res);
      this.collections = res.data;
    });
    this.dialogRef = this.dialogService.open(dialog, { context: data });
  }

  toggle(event, d: any) {
    console.log(event);
    if (event)
      this.chosenMetaData[d[0]] = d[1];
    else
      delete this.chosenMetaData[d[0]];
    console.log(this.chosenMetaData);
  }

  openCollectionDialog(collectionDialog: TemplateRef<any>) {
    this.dataAccess.getCollections().subscribe(res => {
      console.log(res);
      this.collections = res.data;
      this.collectionDialogRef = this.dialogService.open(collectionDialog);
    });
  }


  onCreateCollection() {
    this.dataAccess.createCollection(this.newCollectionName).subscribe(res => {
      if (res.result == 'Success') {
        this.dataAccess.getCollections().subscribe(res => {
          this.collections = res.data;
        });
        this.popover.hide();
      }
    });
  }

  saveAsset() {

    this.dataAccess.saveAssetIntoCollection(this.asset, this.chosenMetaData ,this.chosenCollection, this.searchTerm, this.source, this.scope);
    this.dialogRef.close();
  }

  setChosenCollection(d: any) {
    this.chosenCollection = d;
  }
}
