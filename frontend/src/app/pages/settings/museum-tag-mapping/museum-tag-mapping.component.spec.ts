import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MuseumTagMappingComponent } from './museum-tag-mapping.component';

describe('MuseumTagMappingComponent', () => {
  let component: MuseumTagMappingComponent;
  let fixture: ComponentFixture<MuseumTagMappingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MuseumTagMappingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MuseumTagMappingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
