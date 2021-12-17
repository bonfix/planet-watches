import { TestBed } from '@angular/core/testing';
import {HomeService} from "@pages/home/services/home.service";

describe('HomeService', () => {
  let service: HomeService;

  beforeEach(() => {
    TestBed.configureTestingModule({ teardown: { destroyAfterEach: false } });
    service = TestBed.inject(HomeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
