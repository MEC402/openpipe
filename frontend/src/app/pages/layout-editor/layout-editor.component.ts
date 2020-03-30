
import {Component, OnInit, TemplateRef} from '@angular/core';
import {NbDialogRef, NbDialogService} from "@nebular/theme";
import {DataAccessService} from "../../services/data-access.service";
import {LocalDataSource} from "ng2-smart-table";
import {CdkDragDrop} from "@angular/cdk/drag-drop";

@Component({
  selector: 'ngx-layout-editor',
  templateUrl: './layout-editor.component.html',
  styleUrls: ['./layout-editor.component.scss']
})
export class LayoutEditorComponent implements OnInit {
  leftWallAssets=[];
  centerWallAssets=[];
  rightWallAssets=[];
  wall=1;
  collections=[];
  chosenCollection: any;

  assetsSource: LocalDataSource = new LocalDataSource();

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
  imageConfig: any;

  constructor(private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>,
              protected dialogRefLoad: NbDialogRef<any>,
              protected dialogRefSave: NbDialogRef<any>,
              private dataAccess: DataAccessService) { }

  ngOnInit() {
  }

  offset(element,parent) {
    var parentPos = parent.getBoundingClientRect(),
      childPos = element.getBoundingClientRect(),
      relativePos = {"top":0,"right":0,"left":0,"bottom":0};

    relativePos.top = childPos.top - parentPos.top,
      relativePos.right = childPos.right - parentPos.right,
      relativePos.bottom = childPos.bottom - parentPos.bottom,
      relativePos.left = childPos.left - parentPos.left;

    return relativePos;
  }

  onClick(event: MouseEvent) {
    let leftElements=document.getElementById('leftWall').children;
    let centerElements=document.getElementById('centerWall').children;
    let rightElements=document.getElementById('rightWall').children;

    var divOffset = this.offset(leftElements[0],document.getElementById('leftWall'));
    console.log(divOffset.left, divOffset.top);
  }



  openDialog(dialog: TemplateRef<any>) {
    const data = [];
    this.dataAccess.getCollections().subscribe(res => {
      console.log(res);
      this.collections = res.data;
    });
    this.dialogRef = this.dialogService.open(dialog, { context: data });
  }

  onSelect() {
    console.log(this.chosenCollection);
    this.dataAccess.getPublicAssetsInCollection(this.chosenCollection.id,1,10).subscribe(res => {
      this.assetsSource.load(res.data);
    });
  }

  openLoadDialog(dialog: TemplateRef<any>) {
    const data = [];
    this.dataAccess.getCollections().subscribe(res => {
      console.log(res);
      this.collections = res.data;
    });
    this.dialogRefLoad = this.dialogService.open(dialog, { context: data });
  }

  openSaveDialog(dialog: TemplateRef<any>) {
    this.dialogRefSave = this.dialogService.open(dialog, { context: {}});
  }

  onRowSelect(event: any) {
    if (this.wall == 0) {
      this.leftWallAssets=(event.selected);
    } else if (this.wall == 1) {
      this.centerWallAssets=(event.selected);
    }else if (this.wall == 2) {
      this.rightWallAssets=(event.selected);
    }
    console.log(this.leftWallAssets);
    console.log(this.centerWallAssets);
  }

  onRightClick(r: any, wallnumber) {
    if (wallnumber == 0) {
      this.leftWallAssets = this.arrayRemove(this.leftWallAssets,r);
    } else if (wallnumber == 1) {
      this.centerWallAssets=this.arrayRemove(this.centerWallAssets,r);
    }else if (wallnumber == 2) {
      this.rightWallAssets=this.arrayRemove(this.rightWallAssets,r);
    }
    return false;
  }

  arrayRemove(arr, value) {
    return arr.filter(function(ele){ return ele != value; });
  }

  drop(event: CdkDragDrop<any[], any>) {
    console.log(event);
  }
}







// import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
// import {NbDialogRef, NbDialogService} from "@nebular/theme";
// import {DataAccessService} from "../../services/data-access.service";
// import {LocalDataSource} from "ng2-smart-table";
// import {CdkDragDrop} from "@angular/cdk/drag-drop";
// import {KonvaComponent} from "ng2-konva";
// import {Observable, of} from "rxjs";
// import Konva from "konva";
//
// @Component({
//   selector: 'ngx-layout-editor',
//   templateUrl: './layout-editor.component.html',
//   styleUrls: ['./layout-editor.component.scss']
// })
// export class LayoutEditorComponent implements OnInit {
//   @ViewChild('stage', {static: true}) stage: KonvaComponent;
//   @ViewChild('layer', {static: true}) layer: KonvaComponent;
//
//   public width = 800;
//   public height = 200;
//
//   image= new Image();
//
//   public stageConfig: Observable<any> = of({
//     width: this.width,
//     height: this.height,
//   });
//
//   public imageConfig: Observable<any> = of({
//     width: this.width/10,
//     height: this.height/10,
//     image: this.image,
//     draggable: true,
//   });
//
//
//
// // Konva.Image.fromURL('https://images.metmuseum.org/CRDImages/es/web-large/DP105723.jpg',c => {
// //   this.layer.getStage().add(c);
// //   this.layer.getStage().draw();
// // }),
//
//   constructor() {
//     this.image.src='https://images.metmuseum.org/CRDImages/es/web-large/DP105723.jpg';
//   }
//
//   ngOnInit(): void {
//   }
//
//   onTap(e) {
//     console.log(e)
//     // if click on empty area - remove all transformers
//     if (e.target === this.stage) {
//       this.stage.getStage().find('Transformer').destroy();
//       this.layer.getStage().draw();
//       return;
//     }
//     // do nothing if clicked NOT on our rectangles
//     // if (!e.target.hasName('image')) {
//     //   return;
//     // }
//     // remove old transformers
//     // TODO: we can skip it if current rect is already selected
//     this.stage.getStage().find('Transformer').destroy();
//
//     // create new transformer
//     var tr = new Konva.Transformer();
//     this.layer.getStage().add(tr);
//     tr.attachTo(e.target);
//     this.layer.getStage().draw();
//   }
// }
