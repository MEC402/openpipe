import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TagViewerComponent } from './tag-viewer.component';

describe('TagViewerComponent', () => {
  let component: TagViewerComponent;
  let fixture: ComponentFixture<TagViewerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TagViewerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TagViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
