import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CanonicalMetaTagsComponent } from './canonical-meta-tags.component';

describe('CanonicalMetaTagsComponent', () => {
  let component: CanonicalMetaTagsComponent;
  let fixture: ComponentFixture<CanonicalMetaTagsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CanonicalMetaTagsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CanonicalMetaTagsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
