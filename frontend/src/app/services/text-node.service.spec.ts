import { TestBed } from '@angular/core/testing';

import { TextNodeService } from './text-node.service';

describe('TextNodeService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TextNodeService = TestBed.get(TextNodeService);
    expect(service).toBeTruthy();
  });
});
