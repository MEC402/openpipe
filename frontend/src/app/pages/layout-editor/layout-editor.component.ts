import {Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {TextNodeService} from '../../services/text-node.service';
import Konva from 'konva';
import {ShapeService} from '../../services/shape.service';
import {LocalDataSource} from 'ng2-smart-table';
import { DataAccessService } from 'app/services/data-access.service';
import {NbDialogRef, NbDialogService} from '@nebular/theme';
import {BehaviorSubject} from 'rxjs';


@Component({
  selector: 'ngx-layout-editor',
  templateUrl: './layout-editor.component.html',
  styleUrls: ['./layout-editor.component.scss'],
})
export class LayoutEditorComponent implements OnInit {

  shapesLeft: any = [];
  stageLeft: Konva.Stage;
  layerLeft: Konva.Layer;
  transformersLeft: Konva.Transformer[] = [];


  shapesRight: any = [];
  stageRight: Konva.Stage;
  layerRight: Konva.Layer;
  transformersRight: Konva.Transformer[] = [];


  shapesCenter: any = [];
  stageCenter: Konva.Stage;
  layerCenter: Konva.Layer;
  transformersCenter: Konva.Transformer[] = [];


  selectedShape: any;
  activeWall;

  currentLayer;

  width = 1000;
  height = 800;

  sbl = this.shapeService.rectangle(0, 0, this.width, this.height);
  sbc = this.shapeService.rectangle(0, 0, this.width, this.height);
  sbr = this.shapeService.rectangle(0, 0, this.width, this.height);

  // width = window.innerWidth * 0.9;
  // height = window.innerHeight;

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
    private dataAccess: DataAccessService,
    private shapeService: ShapeService,
    private textNodeService: TextNodeService) {
  }


  ngOnInit() {

    this.dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
  }

  resetWalls() {
    this.stageLeft = new Konva.Stage({
      container: 'container1',
      width: this.width,
      height: this.height,
      id: 'stl',
    });
    this.layerLeft = new Konva.Layer();
    this.stageLeft.add(this.layerLeft);
    this.layerLeft.add(this.sbl);
    this.layerLeft.draw();
    this.stageLeft.on('click', e => this.onStageClick(e));


    this.stageCenter = new Konva.Stage({
      container: 'container2',
      width: this.width,
      height: this.height,
      id: 'stc',
    });
    this.layerCenter = new Konva.Layer();
    this.stageCenter.add(this.layerCenter);
    this.layerCenter.add(this.sbc);
    this.layerCenter.draw();
    this.stageCenter.on('click', e => this.onStageClick(e));

    this.stageRight = new Konva.Stage({
      container: 'container3',
      width: this.width,
      height: this.height,
      id: 'str',
    });
    this.layerRight = new Konva.Layer();
    this.stageRight.add(this.layerRight);
    this.layerRight.add(this.sbr);
    this.layerRight.draw();
    this.stageRight.on('click', e => this.onStageClick(e));

    window.addEventListener('keyup', e => this.onShapeDelete(e));

    this.currentLayer = this.layerLeft;
    this.activeWall = 'Left';
  }


  addText() {
    if (this.activeWall == 'Left') {

      const text = this.textNodeService.textNode(this.stageLeft, this.layerLeft);
      this.shapesLeft.push(text.textNode);
      this.transformersLeft.push(text.tr);

    } else if (this.activeWall == 'Center') {

      const text = this.textNodeService.textNode(this.stageCenter, this.layerCenter);
      this.shapesCenter.push(text.textNode);
      this.transformersCenter.push(text.tr);

    } else if (this.activeWall == 'Right') {

      const text = this.textNodeService.textNode(this.stageRight, this.layerRight);
      this.shapesRight.push(text.textNode);
      this.transformersRight.push(text.tr);
    }
  }

  addImage(asset) {
    const image = this.shapeService.image(asset.openpipe_canonical_smallImage, this.width, this.height);

    image.on('click', e => this.onShapeClick(e));
    image.on('keyup', e => this.onShapeDelete(e));

    this.currentLayer.add(image);
    this.currentLayer.draw();

    if (this.activeWall == 'Left') {
      this.shapesLeft.push({'assetImage' : image , 'assetData' : asset});
    } else if (this.activeWall == 'Center') {
      this.shapesCenter.push({'assetImage' : image , 'assetData' : asset});
    } else if (this.activeWall == 'Right') {
      this.shapesRight.push({'assetImage' : image , 'assetData' : asset});
    }


  }

  onShapeClick (e) {

    if (this.activeWall == 'Left') {

      const n = this.transformersLeft.length;
      if (n > 0) {
        this.transformersLeft[n - 1].detach();
      }
      this.selectedShape = e.target;
      const tr = new Konva.Transformer({
        keepRatio: true,
      });
      this.layerLeft.add(tr);
      tr.attachTo(e.target);
      this.transformersLeft.push(tr);
      this.layerLeft.draw();

    } else if (this.activeWall == 'Center') {

      const n = this.transformersCenter.length;
      if (n > 0) {
        this.transformersCenter[n - 1].detach();
      }
      this.selectedShape = e.target;
      const tr = new Konva.Transformer({
        keepRatio: true,
      });
      this.layerCenter.add(tr);
      tr.attachTo(e.target);
      this.transformersCenter.push(tr);
      this.layerCenter.draw();

    } else if (this.activeWall == 'Right') {
      const n = this.transformersRight.length;
      if (n > 0) {
        this.transformersRight[n - 1].detach();
      }
      this.selectedShape = e.target;
      const tr = new Konva.Transformer({
        keepRatio: true,
      });
      this.layerRight.add(tr);
      tr.attachTo(e.target);
      this.transformersRight.push(tr);
      this.layerRight.draw();
    }
  }

  onShapeDelete(e) {
    if (e.keyCode === 46) {
      if (this.activeWall == 'Left') {

        let index = -1;
        for (let i = 0; i < this.shapesLeft.length; i++) {
          if (this.shapesLeft[i].assetImage == this.selectedShape) {
            index = i;
            break;
          }
        }
        if (index > -1) {
          this.shapesLeft.splice(index, 1);
        }

        this.selectedShape.remove();

        const n = this.transformersLeft.length;
        if (n > 0) {
          this.transformersLeft[n - 1].detach();
        }
        this.layerLeft.batchDraw();

      } else if (this.activeWall == 'Center') {

        let index = -1;
        for (let i = 0; i < this.shapesCenter.length; i++) {
          if (this.shapesCenter[i].assetImage == this.selectedShape) {
            index = i;
            break;
          }
        }
        if (index > -1) {
          this.shapesCenter.splice(index, 1);
        }

        this.selectedShape.remove();

        const n = this.transformersCenter.length;
        if (n > 0) {
          this.transformersCenter[n - 1].detach();
        }
        this.layerCenter.batchDraw();

      } else if (this.activeWall == 'Right') {
        let index = -1;
        for (let i = 0; i < this.shapesRight.length; i++) {
          if (this.shapesRight[i].assetImage == this.selectedShape) {
            index = i;
            break;
          }
        }
        if (index > -1) {
          this.shapesRight.splice(index, 1);
        }

        this.selectedShape.remove();

        const n = this.transformersRight.length;
        if (n > 0) {
          this.transformersRight[n - 1].detach();
        }
        this.layerRight.batchDraw();
      }
    }
  }

  onStageClick(e) {
    if (this.activeWall == 'Left') {

      if (e.target.attrs.id == 'stl') {
        this.selectedShape = null;
        const n = this.transformersLeft.length;
        if (n > 0) {
          this.transformersLeft[n - 1].detach();
        }
      }
      this.layerLeft.draw();

    } else if (this.activeWall == 'Center') {

      if (e.target.attrs.id == 'stl') {
        this.selectedShape = null;
        const n = this.transformersCenter.length;
        if (n > 0) {
          this.transformersCenter[n - 1].detach();
        }
      }
      this.layerCenter.draw();

    } else if (this.activeWall == 'Right') {

      if (e.target.attrs.id == 'stl') {
        this.selectedShape = null;
        const n = this.transformersRight.length;
        if (n > 0) {
          this.transformersRight[n - 1].detach();
        }
      }
      this.layerRight.draw();
    }
  }

  // undo() {
  //   const removedShape = this.shapes.pop();
  //   this.transformers.forEach(t => {
  //     t.detach();
  //   });
  //   if (removedShape) {
  //     removedShape.remove();
  //   }
  //   this.layer.draw();
  // }

  onSelect() {
    this.resetWalls();
    this.dataAccess.getPublicAssetsInCollection(this.chosenCollection.id, 1, 100).subscribe(res => {
      console.log(this.chosenCollection)
      console.log(res);
      this.assetsSource.load(res.data);
    });
  }

  onRowSelect(event: any) {
    if (event.isSelected) {
      this.addImage(event.data);
    } else {
      event.selected.forEach(d => {
        this.addImage(d);
      });
    }
  }

  saveLayout() {
    let resLayout = [];
    resLayout = this.makeLayout(this.shapesLeft, 'left').concat(this.makeLayout(this.shapesCenter, 'center'));
    resLayout = resLayout.concat(this.makeLayout(this.shapesRight, 'right'));
    console.log(resLayout);
    this.dataAccess.saveFolderLayout({"folderId": this.chosenCollection.id[0], "data": resLayout}).subscribe(r=>{
      alert("Layout Saved!");
    });

  }

  makeLayout(shapes, wall) {
    const res = [];
    console.log(shapes)
    shapes.forEach(d => {
      const x = d.assetImage.attrs.x;
      const y = d.assetImage.attrs.y;
      const xs = Number(d.assetImage.attrs.scaleX);
      const ys = Number(d.assetImage.attrs.scaleY);
      const w = Number(d.assetImage.attrs.image.width) * xs;
      const h = Number(d.assetImage.attrs.image.height) * ys;

      console.log(d)

      const e = {
        "assetId": Number(d.assetData.id[0]),
          "guid": 'http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/'
          + d.assetData.id[0],
        "geometry": w.toFixed(2) + ' x ' + h.toFixed(2) + ' + ' + x + ' + ' + y,
        "wall": wall};
      res.push(e);
    });
    return res;
  }

  onChangeTab(e) {
    if (e.tabTitle == 'Left Wall') {
      this.activeWall = 'Left';
      console.log('Left');
      this.currentLayer = this.layerLeft;
    } else if (e.tabTitle == 'Right Wall') {
      this.activeWall = 'Right';
      this.currentLayer = this.layerRight;
      console.log('Right');
    } else if (e.tabTitle == 'Center Wall') {
      this.activeWall = 'Center';
      this.currentLayer = this.layerCenter;
      console.log('Center');
    }

  }
}

