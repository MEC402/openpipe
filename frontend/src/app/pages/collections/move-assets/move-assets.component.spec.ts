import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MoveAssetsComponent } from './move-assets.component';

describe('MoveAssetsComponent', () => {
  let component: MoveAssetsComponent;
  let fixture: ComponentFixture<MoveAssetsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MoveAssetsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MoveAssetsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
