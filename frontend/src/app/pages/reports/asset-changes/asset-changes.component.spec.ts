import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AssetChangesComponent } from './asset-changes.component';

describe('AssetChangesComponent', () => {
  let component: AssetChangesComponent;
  let fixture: ComponentFixture<AssetChangesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AssetChangesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AssetChangesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
