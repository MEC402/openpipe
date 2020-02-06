import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MissingImagesComponent } from './missing-images.component';

describe('MissingImagesComponent', () => {
  let component: MissingImagesComponent;
  let fixture: ComponentFixture<MissingImagesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MissingImagesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MissingImagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
