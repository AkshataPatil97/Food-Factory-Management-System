import { TestBed } from '@angular/core/testing';

import { DeliveryboyService } from './deliveryboy.service';

describe('DeliveryboyService', () => {
  let service: DeliveryboyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DeliveryboyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
