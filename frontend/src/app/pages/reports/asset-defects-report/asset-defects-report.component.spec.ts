import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AssetDefectsReportComponent } from './asset-defects-report.component';

describe('AssetDefectsReportComponent', () => {
  let component: AssetDefectsReportComponent;
  let fixture: ComponentFixture<AssetDefectsReportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AssetDefectsReportComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AssetDefectsReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
