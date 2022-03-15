import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NbOAuth2LoginComponent } from './oauth2-login.component';

describe('NbOAuth2LoginComponent', () => {
  let component: NbOAuth2LoginComponent;
  let fixture: ComponentFixture<NbOAuth2LoginComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NbOAuth2LoginComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NbOAuth2LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
