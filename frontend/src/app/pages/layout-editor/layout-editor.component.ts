import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {NbDialogRef, NbDialogService} from '@nebular/theme';
import {DataAccessService} from '../../services/data-access.service';
import {LocalDataSource} from 'ng2-smart-table';
import {CdkDragDrop} from '@angular/cdk/drag-drop';
import {Observable, of} from 'rxjs';
import {KonvaComponent} from 'ng2-konva';

@Component({
  selector: 'ngx-layout-editor',
  templateUrl: './layout-editor.component.html',
  styleUrls: ['./layout-editor.component.scss'],
})
export class LayoutEditorComponent implements OnInit {
  @ViewChild('stage', {'static': false}) stage: KonvaComponent;
  @ViewChild('layer', {'static': false}) layer: KonvaComponent;

  leftWallAssets = [];
  centerWallAssets = [];
  rightWallAssets = [];
  wall = 1;
  collections = [];
  chosenCollection: any;

  assetsSource: LocalDataSource = new LocalDataSource();

  public configStage: Observable<any> = of({
    width: 200,
    height: 200,
  });


  assetsSettings = {
    selectMode: 'multi',
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

  constructor(private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>,
              protected dialogRefLoad: NbDialogRef<any>,
              protected dialogRefSave: NbDialogRef<any>,
              private dataAccess: DataAccessService) {
  }

  ngOnInit() {

  }

  offset(element, parent) {
    const parentPos = parent.getBoundingClientRect(),
      childPos = element.getBoundingClientRect(),
      relativePos = {'top': 0, 'right': 0, 'left': 0, 'bottom': 0};

    relativePos.top = childPos.top - parentPos.top,
      relativePos.right = childPos.right - parentPos.right,
      relativePos.bottom = childPos.bottom - parentPos.bottom,
      relativePos.left = childPos.left - parentPos.left;

    return relativePos;
  }

  onClick(event: MouseEvent) {
    const leftElements = document.getElementById('leftWall').children;
    const centerElements = document.getElementById('centerWall').children;
    const rightElements = document.getElementById('rightWall').children;

    const divOffset = this.offset(leftElements[0], document.getElementById('leftWall'));
    console.log(divOffset.left, divOffset.top);
  }

  onSelect() {
    this.dataAccess.getPublicAssetsInCollection(this.chosenCollection.id, 1, 10).subscribe(res => {
      this.assetsSource.load(res.data);
    });
  }

  openLoadDialog(dialog: TemplateRef<any>) {
    const data = [];
    this.dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
    this.dialogRefLoad = this.dialogService.open(dialog, {context: data});
  }

  openSaveDialog(dialog: TemplateRef<any>) {
    this.dialogRefSave = this.dialogService.open(dialog, {context: {}});
  }

  onRowSelect(event: any) {
    if (this.wall == 0) {
      this.leftWallAssets = (event.selected);
    } else if (this.wall == 1) {
      this.centerWallAssets = (event.selected);
      this.centerWallAssets.forEach(d => {
        d.config = of({
          x: 0,
          y: 10,
          width: 50,
          image: d.openpipe_canonical_smallImage[0],
        });
      });
      console.log(this.centerWallAssets);
    } else if (this.wall == 2) {
      this.rightWallAssets = (event.selected);
    }
    this.layer.getStage().draw();
  }

  onRightClick(r: any, wallnumber) {
    if (wallnumber == 0) {
      this.leftWallAssets = this.arrayRemove(this.leftWallAssets, r);
    } else if (wallnumber == 1) {
      this.centerWallAssets = this.arrayRemove(this.centerWallAssets, r);
    } else if (wallnumber == 2) {
      this.rightWallAssets = this.arrayRemove(this.rightWallAssets, r);
    }
    return false;
  }

  arrayRemove(arr, value) {
    return arr.filter(function (ele) {
      return ele != value;
    });
  }

  drop(event: CdkDragDrop<any[], any>) {
    console.log(event);
  }
}
