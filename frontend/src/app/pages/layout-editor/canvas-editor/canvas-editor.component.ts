import { Component, OnInit } from '@angular/core';
import Konva from 'konva';
import {LocalDataSource} from 'ng2-smart-table';
import {NbDialogRef, NbDialogService} from '@nebular/theme';
import {DataAccessService} from '../../../services/data-access.service';
import {ShapeService} from '../../../services/shape.service';
import {TextNodeService} from '../../../services/text-node.service';

@Component({
  selector: 'ngx-canvas-editor',
  templateUrl: './canvas-editor.component.html',
  styleUrls: ['./canvas-editor.component.scss'],
})
export class CanvasEditorComponent implements OnInit {

  shapes: any = [];
  stage: Konva.Stage;
  layer: Konva.Layer;
  transformers: Konva.Transformer[] = [];
  selectedShape: any;

  // width = window.innerWidth * 0.9;
  // height = window.innerHeight;

  width = 800;
  height = 600;

  collections = [];


  constructor(private shapeService: ShapeService,
    private textNodeService: TextNodeService) {
  }


  ngOnInit() {

    this.stage = new Konva.Stage({
      container: 'container1',
      width: this.width,
      height: this.height,
      id: 'stl',
    });
    this.layer = new Konva.Layer();
    this.stage.add(this.layer);
    const sb = this.shapeService.rectangle(0, 0, this.width, this.height);
    this.layer.add(sb);
    this.layer.draw();

    this.stage.on('click', e => this.onStageClick(e));
    window.addEventListener('keyup', e => this.onShapeDelete(e));
  }


  addText() {
    const text = this.textNodeService.textNode(this.stage, this.layer);
    this.shapes.push(text.textNode);
    this.transformers.push(text.tr);
  }

  addImage(asset) {
    const image = this.shapeService.image(asset.openpipe_canonical_smallImage, this.width, this.height);

    image.on('click', e => this.onShapeClick(e));
    image.on('keyup', e => this.onShapeDelete(e));

    this.layer.add(image);
    this.shapes.push({'assetImage' : image , 'assetData' : asset});
    this.layer.draw();
  }

  onShapeClick (e) {
    const n = this.transformers.length;
    if (n > 0) {
      this.transformers[n - 1].detach();
    }
    this.selectedShape = e.target;
    const tr = new Konva.Transformer({
      keepRatio: true,
    });
    this.layer.add(tr);
    tr.attachTo(e.target);
    this.transformers.push(tr);
    this.layer.draw();
  }

  onShapeDelete(e) {
    if (e.keyCode === 46) {
      let index = -1;
      for (let i = 0; i < this.shapes.length; i++) {
        if (this.shapes[i].assetImage == this.selectedShape) {
          index = i;
          break;
        }
      }
      if (index > -1) {
        this.shapes.splice(index, 1);
      }

      this.selectedShape.remove();

      const n = this.transformers.length;
      if (n > 0) {
        this.transformers[n - 1].detach();
      }
      this.layer.batchDraw();
    }
  }

  onStageClick(e) {
    if (e.target.attrs.id == 'stl') {
      this.selectedShape = null;
      const n = this.transformers.length;
      if (n > 0) {
        this.transformers[n - 1].detach();
      }
    }
    this.layer.draw();
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

  addTransformerListeners(inputShape) {
    const component = this;
    console.log(component);
    const tr = new Konva.Transformer({
      keepRatio: true,
    });
    this.stage.on('click', function (e) {
      console.log(this);
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
        return;
      }
    });
  }

  addDeleteListener(shape) {
    const component = this;
    window.addEventListener('keydown', function (e) {
      if (e.keyCode === 46) {
        // shape.remove();
        // component.transformers.forEach(t => {
        //   t.detach();
        // });
        console.log(shape._id);

        const selectedShape = component.shapes.find(s => s._id == shape._id);
        selectedShape.remove();
        e.preventDefault();
      }
      component.layer.batchDraw();
    });
  }


}
