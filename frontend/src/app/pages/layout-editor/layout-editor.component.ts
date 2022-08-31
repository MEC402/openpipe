import {ChangeDetectionStrategy, Component, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {TextNodeService} from '../../services/text-node.service';
import Konva from 'konva';
import {ShapeService} from '../../services/shape.service';
import {LocalDataSource} from 'ng2-smart-table';
import { DataAccessService } from 'app/services/data-access.service';
import {NbDialogRef, NbDialogService} from '@nebular/theme';
import {BehaviorSubject} from 'rxjs';
import {log} from "util";


@Component({
  selector: 'ngx-layout-editor',
  templateUrl: './layout-editor.component.html',
  styleUrls: ['./layout-editor.component.scss'],
})
export class LayoutEditorComponent implements OnInit {

  shapesLeft: any = [];
  stage: Konva.Stage;
  transformersLeft: Konva.Transformer[] = [];


  shapesRight: any = [];
  transformersRight: Konva.Transformer[] = [];


  shapesCenter: any = [];
  transformersCenter: Konva.Transformer[] = [];


  selectedShape: any;
  activeWall;

  currentLayer;

  // 2160px high.
  // Total width: 21802px.
  // Left/East: 7266px.
  // Center/South: 6065px.
  // Right/West: 8480px.

  width =  7266;
  height = 2160;
  // width =  1000;
  // height = 1000;

  zoom: number;

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

    this.zoom = 0.2;

    this.stage = new Konva.Stage({
      container: 'container1',
      width: this.width,
      height: this.height,
      id: 'stl',
    });

    this.stage.scale({ x: this.zoom, y: this.zoom });

    this.stage.on('click', e => this.onStageClick(e));
    window.addEventListener('keyup', e => this.onShapeDelete(e));
    this.activeWall = 'Left';

    this.currentLayer = new Konva.Layer();

    this.stage.add(this.currentLayer);
    this.dataAccess.getFolders(1, 200).subscribe(res => {
      this.collections = res.data;
    });
  }

  onSelect() {

    this.resetWalls();
    this.dataAccess.getFolderAssets(this.chosenCollection.id, 1, 100).subscribe(res => {
      this.assetsSource.load(res.data);
    });
    this.dataAccess.loadFolderLayout(this.chosenCollection.id).subscribe(res => {
      res.data.forEach(d => {
        const geoData = d.geometry.split(' ');
        this.addImage(d, geoData[4], geoData[6], geoData[0], geoData[2]);
      });
      this.changeWall('l');
    });
  }

  resetWalls() {
  }


  addImage(asset, x, y, w , h) {
    const image = this.shapeService.image(asset.image, x, y, w, h);

    image.on('click', e => this.onShapeClick(e));
    image.on('keyup', e => this.onShapeDelete(e));

    if (asset.wall.toLowerCase() == 'left') {
      this.shapesLeft.push({'assetImage' : image , 'assetData' : asset});
    } else if (asset.wall.toLowerCase() == 'center') {
      this.shapesCenter.push({'assetImage' : image , 'assetData' : asset});
    } else if (asset.wall.toLowerCase() == 'right') {
      this.shapesRight.push({'assetImage' : image , 'assetData' : asset});
    }
  }

  onShapeClick (e) {
    console.log("click");
    console.log(e);
    if (this.activeWall == 'Left') {

      const n = this.transformersLeft.length;
      if (n > 0) {
        this.transformersLeft[n - 1].detach();
      }
      this.selectedShape = e.target;
      const tr = new Konva.Transformer({
        keepRatio: true,
      });
      this.currentLayer.add(tr);
      tr.attachTo(e.target);
      this.transformersLeft.push(tr);
      this.currentLayer.draw();
    }

    // } else if (this.activeWall == 'Center') {
    //
    //   const n = this.transformersCenter.length;
    //   if (n > 0) {
    //     this.transformersCenter[n - 1].detach();
    //   }
    //   this.selectedShape = e.target;
    //   const tr = new Konva.Transformer({
    //     keepRatio: true,
    //   });
    //   this.layerCenter.add(tr);
    //   tr.attachTo(e.target);
    //   this.transformersCenter.push(tr);
    //   this.layerCenter.draw();
    //
    // } else if (this.activeWall == 'Right') {
    //   const n = this.transformersRight.length;
    //   if (n > 0) {
    //     this.transformersRight[n - 1].detach();
    //   }
    //   this.selectedShape = e.target;
    //   const tr = new Konva.Transformer({
    //     keepRatio: true,
    //   });
    //   this.layerRight.add(tr);
    //   tr.attachTo(e.target);
    //   this.transformersRight.push(tr);
    //   this.layerRight.draw();
    // }
  }

  onShapeDelete(e) {
    // if (e.keyCode === 46) {
    //   if (this.activeWall == 'Left') {
    //
    //     let index = -1;
    //     for (let i = 0; i < this.shapesLeft.length; i++) {
    //       if (this.shapesLeft[i].assetImage == this.selectedShape) {
    //         index = i;
    //         break;
    //       }
    //     }
    //     if (index > -1) {
    //       this.shapesLeft.splice(index, 1);
    //     }
    //
    //     this.selectedShape.remove();
    //
    //     const n = this.transformersLeft.length;
    //     if (n > 0) {
    //       this.transformersLeft[n - 1].detach();
    //     }
    //     this.layerLeft.batchDraw();
    //
    //   } else if (this.activeWall == 'Center') {
    //
    //     let index = -1;
    //     for (let i = 0; i < this.shapesCenter.length; i++) {
    //       if (this.shapesCenter[i].assetImage == this.selectedShape) {
    //         index = i;
    //         break;
    //       }
    //     }
    //     if (index > -1) {
    //       this.shapesCenter.splice(index, 1);
    //     }
    //
    //     this.selectedShape.remove();
    //
    //     const n = this.transformersCenter.length;
    //     if (n > 0) {
    //       this.transformersCenter[n - 1].detach();
    //     }
    //     this.layerCenter.batchDraw();
    //
    //   } else if (this.activeWall == 'Right') {
    //     let index = -1;
    //     for (let i = 0; i < this.shapesRight.length; i++) {
    //       if (this.shapesRight[i].assetImage == this.selectedShape) {
    //         index = i;
    //         break;
    //       }
    //     }
    //     if (index > -1) {
    //       this.shapesRight.splice(index, 1);
    //     }
    //
    //     this.selectedShape.remove();
    //
    //     const n = this.transformersRight.length;
    //     if (n > 0) {
    //       this.transformersRight[n - 1].detach();
    //     }
    //     this.layerRight.batchDraw();
    //   }
    // }
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
    } else if (this.activeWall == 'Center') {

      if (e.target.attrs.id == 'stl') {
        this.selectedShape = null;
        const n = this.transformersCenter.length;
        if (n > 0) {
          this.transformersCenter[n - 1].detach();
        }
      }
    } else if (this.activeWall == 'Right') {

      if (e.target.attrs.id == 'stl') {
        this.selectedShape = null;
        const n = this.transformersRight.length;
        if (n > 0) {
          this.transformersRight[n - 1].detach();
        }
      }
    }
    this.currentLayer.draw();
  }



  onRowSelect(event: any) {
    if (event.isSelected) {
      this.addImage(event.data, 10, 10, 100, 100);
    } else {
      event.selected.forEach(d => {
        this.addImage(d, 10, 10, 100, 100);
      });
    }
  }

  saveLayout() {
    let resLayout = [];
    resLayout = this.makeLayout(this.shapesLeft, 'left').concat(this.makeLayout(this.shapesCenter, 'center'));
    resLayout = resLayout.concat(this.makeLayout(this.shapesRight, 'right'));
    console.log(resLayout);
    this.dataAccess.saveFolderLayout({'folderId': this.chosenCollection.id[0], 'data': resLayout}).subscribe(r => {
      alert('Layout Saved!');
    });

  }

  makeLayout(shapes, wall) {
    const res = [];
    console.log(shapes);
    shapes.forEach(d => {
      const x = d.assetImage.attrs.x;
      const y = d.assetImage.attrs.y;
      const xs = Number(d.assetImage.attrs.scaleX);
      const ys = Number(d.assetImage.attrs.scaleY);
      const w = Number(d.assetImage.attrs.image.width) * xs;
      const h = Number(d.assetImage.attrs.image.height) * ys;

      console.log(d);

      const e = {
        'assetId': Number(d.assetData.assetId),
          'guid': 'http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/'
          + d.assetData.assetId,
        'geometry': w.toFixed(2) + ' x ' + h.toFixed(2) + ' + ' + x + ' + ' + y,
        'wall': wall};
      res.push(e);
    });
    return res;
  }


  changeWall(wallAbr: string) {
    if (wallAbr === 'l') {
      this.activeWall = 'Left';
      this.drawShapesInCurrentLayer(this.shapesLeft);
    } else if (wallAbr === 'c') {
      this.activeWall = 'Center';
      this.drawShapesInCurrentLayer(this.shapesCenter);
    } else if (wallAbr === 'r') {
      this.activeWall = 'Right';
      this.drawShapesInCurrentLayer(this.shapesRight);
    }
    this.currentLayer.draw();
  }


  drawShapesInCurrentLayer(shapes) {
    console.log(shapes);
    this.currentLayer.removeChildren();
    this.currentLayer.add(this.sbl);

    shapes.forEach( s => {
      this.currentLayer.add(s.assetImage);
      this.currentLayer.draw();
    });
  }

  changeZoom() {
    this.stage.scale({ x: this.zoom, y: this.zoom });
    this.currentLayer.draw();

  }
}

