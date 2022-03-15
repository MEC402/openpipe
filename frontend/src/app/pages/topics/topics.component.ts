import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ngx-topics',
  templateUrl: './topics.component.html',
  styleUrls: ['./topics.component.scss'],
})
export class TopicsComponent implements OnInit {

  topicNames = [
    {'name': 'artist', 'code': '400'},
    {'name': 'city', 'code': '500'},
    {'name': 'classification', 'code': '600'},
    {'name': 'culture', 'code': '700'},
    {'name': 'genre', 'code': '800'},
    {'name': 'medium', 'code': '900'},
    {'name': 'nation', 'code': 'a00'},
    {'name': 'title', 'code': 'f00'},
  ];


  constructor() { }

  ngOnInit() {

  }

}
