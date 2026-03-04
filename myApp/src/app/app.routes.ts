import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./home/home.page').then(m => m.HomePage)
  },
  {
    path: 'gigs',
    loadComponent: () =>
      import('./features/gigs/gigs.page').then(m => m.GigsPage)
  },
  {
    path: 'store',
    loadComponent: () =>
      import('./features/store/store.page').then(m => m.StorePage)
  },
  {
    path: 'auth',
    loadChildren: () =>
      import('./features/auth/auth.routes').then(m => m.AUTH_ROUTES)
  }
];