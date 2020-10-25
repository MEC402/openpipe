import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CellDropDownComponent } from './cell-drop-down.component';

describe('CellDropDownComponent', () => {
  let component: CellDropDownComponent;
  let fixture: ComponentFixture<CellDropDownComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CellDropDownComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CellDropDownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
