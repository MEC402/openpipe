import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AssetTagCardComponent } from './asset-tag-card.component';

describe('AssetTagCardComponent', () => {
  let component: AssetTagCardComponent;
  let fixture: ComponentFixture<AssetTagCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AssetTagCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AssetTagCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
