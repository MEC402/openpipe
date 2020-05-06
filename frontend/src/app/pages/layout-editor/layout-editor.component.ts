import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {TextNodeService} from '../../services/text-node.service';
import Konva from 'konva';
import {ShapeService} from '../../services/shape.service';
import {LocalDataSource} from 'ng2-smart-table';
import { DataAccessService } from 'app/services/data-access.service';
import {NbDialogRef, NbDialogService} from "@nebular/theme";
import {BehaviorSubject} from "rxjs";


@Component({
  selector: 'ngx-layout-editor',
  templateUrl: './layout-editor.component.html',
  styleUrls: ['./layout-editor.component.scss'],
})
export class LayoutEditorComponent implements OnInit {
  shapes: any = [];
  stage: Konva.Stage;
  layer: Konva.Layer;
  transformers: Konva.Transformer[] = [];

  collections = [];
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

  constructor(
    private dialogService: NbDialogService,
    private dataAccess: DataAccessService,
    private shapeService: ShapeService,
    private textNodeService: TextNodeService,
    protected dialogRefLoad: NbDialogRef<any>) {}


  ngOnInit() {
    const width = window.innerWidth * 0.9;
    const height = window.innerHeight;
    this.stage = new Konva.Stage({
      container: 'container',
      width: width,
      height: height,
    });
    this.layer = new Konva.Layer();
    this.stage.add(this.layer);
  }


  addText() {
    const text = this.textNodeService.textNode(this.stage, this.layer);
    this.shapes.push(text.textNode);
    this.transformers.push(text.tr);
  }

  addImage(url) {
    const image = this.shapeService.image(url);
    this.layer.add(image);
    this.shapes.push(image);
    this.stage.add(this.layer);
    this.addTransformerListeners();
  }

  undo() {
    const removedShape = this.shapes.pop();
    this.transformers.forEach(t => {
      t.detach();
    });
    if (removedShape) {
      removedShape.remove();
    }
    this.layer.draw();
  }
  addTransformerListeners() {
    const component = this;
    const tr = new Konva.Transformer({
      keepRatio: true,
    });
    this.stage.on('click', function (e) {
      if (!this.clickStartShape) {
        return;
      }
      if (e.target._id == this.clickStartShape._id) {
        component.addDeleteListener(e.target);
        component.layer.add(tr);
        tr.attachTo(e.target);
        component.transformers.push(tr);
        component.layer.draw();
      } else {
        tr.detach();
        component.layer.draw();
      }
    });
  }

  addDeleteListener(shape) {
    const component = this;
    window.addEventListener('keydown', function (e) {
      if (e.keyCode === 46) {
        shape.remove();
        component.transformers.forEach(t => {
          t.detach();
        });
        const selectedShape = component.shapes.find(s => s._id == shape._id);
        selectedShape.remove();
        e.preventDefault();
      }
      component.layer.batchDraw();
    });
  }

  onSelect() {
    this.dataAccess.getPublicAssetsInCollection(this.chosenCollection.id, 1, 10).subscribe(res => {
      this.assetsSource.load(res.data);
    });
  }

  onRowSelect(event: any) {
    event.selected.forEach(d => {
      this.addImage(d.openpipe_canonical_smallImage);
    });
  }

  openLoadDialog(dialog: TemplateRef<any>) {
    const data = [];
    this.dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
    this.dialogRefLoad = this.dialogService.open(dialog, {context: data});
  }
}




// @ViewChild('stage', {'static': false}) stage: KonvaComponent;
// @ViewChild('layer', {'static': false}) layer: KonvaComponent;
//
// leftWallAssets = [];
// centerWallAssets = [];
// rightWallAssets = [];
// wall = 1;
// collections = [];
// chosenCollection: any;
//
// assetsSource: LocalDataSource = new LocalDataSource();
//
// public configStage: Observable<any> = of({
//   width: 800,
//   height: 500,
// });


// assetsSettings = {
//   selectMode: 'multi',
//   actions: false,
//   columns: {
//     openpipe_canonical_smallImage: {
//       filter: false,
//       title: 'Picture',
//       type: 'html',
//       valuePrepareFunction: (openpipe_canonical_smallImage) => {
//         return '<img width="50px" src="' + openpipe_canonical_smallImage[0] + '" />';
//       },
//     },
//     openpipe_canonical_title: {
//       title: 'Title',
//       type: 'string',
//     },
//   },
// };
//
// constructor(private dialogService: NbDialogService,
//   protected dialogRef: NbDialogRef<any>,
//   protected dialogRefLoad: NbDialogRef<any>,
//   protected dialogRefSave: NbDialogRef<any>,
//   private dataAccess: DataAccessService) {
// }
//
// ngOnInit() {
//
// }
//
// offset(element, parent) {
//   const parentPos = parent.getBoundingClientRect(),
//     childPos = element.getBoundingClientRect(),
//     relativePos = {'top': 0, 'right': 0, 'left': 0, 'bottom': 0};
//
//   relativePos.top = childPos.top - parentPos.top,
//     relativePos.right = childPos.right - parentPos.right,
//     relativePos.bottom = childPos.bottom - parentPos.bottom,
//     relativePos.left = childPos.left - parentPos.left;
//
//   return relativePos;
// }
//
// onClick(event: MouseEvent) {
//   const leftElements = document.getElementById('leftWall').children;
//   const centerElements = document.getElementById('centerWall').children;
//   const rightElements = document.getElementById('rightWall').children;
//
//   const divOffset = this.offset(leftElements[0], document.getElementById('leftWall'));
//   console.log(divOffset.left, divOffset.top);
// }
//
// onSelect() {
//   this.dataAccess.getPublicAssetsInCollection(this.chosenCollection.id, 1, 10).subscribe(res => {
//     this.assetsSource.load(res.data);
//   });
// }
// onRowSelect(event: any) {
//   if (this.wall == 0) {
//     this.leftWallAssets = (event.selected);
//   } else if (this.wall == 1) {
//     this.centerWallAssets = (event.selected);
//     this.centerWallAssets.forEach(d => {
//       d.config = new BehaviorSubject ({
//         x: 0,
//         y: 10,
//         width: 50,
//         image: d.openpipe_canonical_smallImage[0],
//       });
//     });
//     console.log(this.centerWallAssets);
//   } else if (this.wall == 2) {
//     this.rightWallAssets = (event.selected);
//   }
//   this.layer.getStage().draw();
// }
//
// openLoadDialog(dialog: TemplateRef<any>) {
//   const data = [];
//   this.dataAccess.getCollections().subscribe(res => {
//     this.collections = res.data;
//   });
//   this.dialogRefLoad = this.dialogService.open(dialog, {context: data});
// }
//
// openSaveDialog(dialog: TemplateRef<any>) {
//   this.dialogRefSave = this.dialogService.open(dialog, {context: {}});
// }
//

//
// onRightClick(r: any, wallnumber) {
//   if (wallnumber == 0) {
//     this.leftWallAssets = this.arrayRemove(this.leftWallAssets, r);
//   } else if (wallnumber == 1) {
//     this.centerWallAssets = this.arrayRemove(this.centerWallAssets, r);
//   } else if (wallnumber == 2) {
//     this.rightWallAssets = this.arrayRemove(this.rightWallAssets, r);
//   }
//   return false;
// }
//
// arrayRemove(arr, value) {
//   return arr.filter(function (ele) {
//     return ele != value;
//   });
// }
//
// drop(event: CdkDragDrop<any[], any>) {
//   console.log(event);
// }
