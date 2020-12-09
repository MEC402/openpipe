import { Injectable } from '@angular/core';
import Konva from 'konva';
import {circle, control} from 'leaflet';
import scale = control.scale;

@Injectable({
  providedIn: 'root',
})
export class ShapeService {

  constructor() { }

  image(url,sw,sh) {
    const img = new Image();
    img.src = url;
    return new Konva.Image({
      image: img,
      x: 10,
      y: 10,
      draggable: true,
      scaleX: 0.5,
      scaleY: 0.5,
      dragBoundFunc: function (pos) {
        return {
          x: pos.x < 0 ? 0 : pos.x,
          y: pos.y < 0 ? 0 : pos.y,
        };
      },
    });
  }

  circle() {
    return new Konva.Circle({
      x: 100,
      y: 100,
      radius: 70,
      fill: 'red',
      stroke: 'black',
      strokeWidth: 4,
      draggable: true,
    });
  }

  line(pos, mode: string = 'brush') {
    return new Konva.Line({
      stroke: '#df4b26',
      strokeWidth: 5,
      globalCompositeOperation:
        mode === 'brush' ? 'source-over' : 'destination-out',
      points: [pos.x, pos.y],
      draggable: mode == 'brush',
    });
  }

  rectangle(x, y, w, h) {
    return new Konva.Rect({
      x: x,
      y: y,
      width: w,
      height: h,
      stroke: 'black',
      strokeWidth: 4,
      draggable: false,
    });
  }
}
