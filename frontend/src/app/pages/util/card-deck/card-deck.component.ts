import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'ngx-card-deck',
  templateUrl: './card-deck.component.html',
  styleUrls: ['./card-deck.component.scss']
})
export class CardDeckComponent implements OnInit {

  paginatorSize=10;
  numberOfProductsDisplayedInPage=5;
  @Input() assets: any;
  @Input() source;
  @Input() searchTerm;

  constructor() {
  }

  ngOnInit() {
    console.log(this.source);
  }

  updateProductsDisplayedInPage($event) {
    console.log('updateProductsDisplayedInPage');
  }
}
