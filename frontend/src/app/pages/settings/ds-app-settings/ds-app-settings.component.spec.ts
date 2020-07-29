import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DsAppSettingsComponent } from './ds-app-settings.component';

describe('DsAppSettingsComponent', () => {
  let component: DsAppSettingsComponent;
  let fixture: ComponentFixture<DsAppSettingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DsAppSettingsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DsAppSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
