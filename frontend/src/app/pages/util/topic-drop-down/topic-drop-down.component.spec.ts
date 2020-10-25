import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicDropDownComponent } from './topic-drop-down.component';

describe('TopicDropDownComponent', () => {
  let component: TopicDropDownComponent;
  let fixture: ComponentFixture<TopicDropDownComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopicDropDownComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopicDropDownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
