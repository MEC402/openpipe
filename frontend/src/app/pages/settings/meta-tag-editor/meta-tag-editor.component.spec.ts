import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MetaTagEditorComponent } from './meta-tag-editor.component';

describe('MetaTagEditorComponent', () => {
  let component: MetaTagEditorComponent;
  let fixture: ComponentFixture<MetaTagEditorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MetaTagEditorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MetaTagEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
