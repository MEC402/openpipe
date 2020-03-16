import {Component, OnInit, TemplateRef} from '@angular/core';
import {NbDialogRef, NbDialogService} from "@nebular/theme";
import {DataAccessService} from "../../services/data-access.service";

@Component({
  selector: 'ngx-layout-editor',
  templateUrl: './layout-editor.component.html',
  styleUrls: ['./layout-editor.component.scss']
})
export class LayoutEditorComponent implements OnInit {
  leftWallAssets=[];
  centerWallAssets=[];
  rightWallAssets=[];

  constructor(private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>,
              private dataAccess: DataAccessService) { }

  ngOnInit() {
  }

  onClick(event: MouseEvent) {
    console.log(event);
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
}
