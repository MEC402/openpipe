import { Injectable } from '@angular/core';
import Konva from 'konva';
import {circle, control} from 'leaflet';
import scale = control.scale;

@Injectable({
  providedIn: 'root',
})
export class ShapeService {

  constructor() { }

  image(url, x, y, w, h) {
    const img = new Image();
    img.src = url;
    img.onerror = function () {
      img.src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Picture_icon_BLACK.svg/149px-Picture_icon_BLACK.svg.png';
    };
    return new Konva.Image({
      image: img,
      x: Math.ceil(x),
      y: Math.ceil(y),
      draggable: true,
      // scaleX: 0.5,
      // scaleY: 0.5,
      width: Math.ceil(w),
      height: Math.ceil(h),
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
