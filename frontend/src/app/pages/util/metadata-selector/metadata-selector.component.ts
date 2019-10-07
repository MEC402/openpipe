import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'ngx-metadata-selector',
  templateUrl: './metadata-selector.component.html',
  styleUrls: ['./metadata-selector.component.scss']
})
export class MetadataSelectorComponent implements OnInit {

  @Input() metaTags;
  chosenMetaData={};
  constructor() { }

  ngOnInit() {
  }
  toggle(event, d: any) {
    console.log(d);
    if (event)
      this.chosenMetaData[d[0]] = d[1];
    else
      delete this.chosenMetaData[d[0]];
  }
}
