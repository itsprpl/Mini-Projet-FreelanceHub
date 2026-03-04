import { Injectable } from '@angular/core';
import { of } from 'rxjs';

@Injectable()
export class ApiService {
  private mock = true;

  constructor() {}

  // Auth
  login(email: string, password: string) {
    if (this.mock) {
      return of({ token: 'mock-token', user: { id: 'u1', email, role: 'freelancer', status: 'approved' } });
    }
    // real implementation -> HttpClient
    throw new Error('Not implemented');
  }

  register(payload: any) {
    if (this.mock) return of({ ok: true, userId: 'u1' });
    throw new Error('Not implemented');
  }

  getGigs() {
    if (this.mock) return of([
      { id: 'g1', title: 'I will build a REST API', price: 100 },
      { id: 'g2', title: 'I will design your landing page', price: 80 }
    ]);
    throw new Error('Not implemented');
  }

  getProducts() {
    if (this.mock) return of([
      { id: 'p1', title: 'Starter Kit: Angular Boilerplate', price: 25, version: '1.0' }
    ]);
    throw new Error('Not implemented');
  }
}