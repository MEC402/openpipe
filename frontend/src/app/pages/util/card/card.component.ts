import {Component, Input, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {NbDialogRef, NbDialogService, NbPopoverDirective, NbWindowService} from '@nebular/theme';
import {DataAccessService} from '../../../services/data-access.service';
import {LocalDataSource} from "ng2-smart-table";

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

  settings = {
    selectMode: 'multi',
    pager: {
      display: true,
      perPage: 10,
    },
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
      confirmSave : true,
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

  assetsSource: LocalDataSource = new LocalDataSource();


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
    })
    let temp=[];
    data.forEach(d=>{
      if (d[0] != 'id' && d[0]!='metaDataId')
        temp.push({'tagName': d[0], 'value': d[1]});

    });
    this.assetsSource.load(temp);

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
    this.popover.hide();
    this.dataAccess.createCollection(this.newCollectionName).subscribe(res => {
      this.dataAccess.getCollections().subscribe(resp => {
        this.collections = resp.data;
      });
    });
  }

  saveAsset() {
    console.log(this.chosenCollection.id[0]);
    this.dataAccess.saveAssetIntoCollection(this.asset, this.chosenMetaData ,this.chosenCollection, this.searchTerm, this.source, this.scope);
    this.dialogRef.close();
  }

  setChosenCollection(d: any) {
    this.chosenCollection = d;
  }

  onRowSelect(event: any) {
    console.log(event);
  }
}
