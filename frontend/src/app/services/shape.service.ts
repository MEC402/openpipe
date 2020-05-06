import { Injectable } from '@angular/core';
import Konva from 'konva';
import {circle} from 'leaflet';

@Injectable({
  providedIn: 'root',
})
export class ShapeService {

  constructor() { }

  image(url) {
    const img = new Image();
    img.src = url;
    return new Konva.Image({
      image: img,
      draggable: true,
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

  rectangle() {
    return new Konva.Rect({
      x: 20,
      y: 20,
      width: 100,
      height: 50,
      fill: 'green',
      stroke: 'black',
      strokeWidth: 4,
      draggable: true,
    });
  }
}
