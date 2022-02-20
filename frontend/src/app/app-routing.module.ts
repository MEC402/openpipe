import { ExtraOptions, RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import {
  NbAuthComponent,
  NbLoginComponent,
  NbLogoutComponent,
  NbRegisterComponent,
  NbRequestPasswordComponent,
  NbResetPasswordComponent,
} from '@nebular/auth';
import {OAuth2LoginComponent} from './oauth2-login/oauth2-login.component';
import {OAuth2CallbackComponent} from './oauth2-callback/oauth2-callback.component';
import {AuthGuardService} from './services/auth-guard.service';

const routes: Routes = [
  {
    path: 'pages',
    canActivate: [AuthGuardService],
    loadChildren: () => import('app/pages/pages.module')
      .then(m => m.PagesModule),
  },
   { path: '', redirectTo: 'auth', pathMatch: 'full' },
  // { path: '**', redirectTo: 'pages' },
  {
    path: 'auth',
    component: NbAuthComponent,
    children: [
      {
        path: '',
        component: OAuth2LoginComponent,
      },
      {
        path: 'callback',
        component: OAuth2CallbackComponent,
      },
    ],
  },
];

const config: ExtraOptions = {
  useHash: false,
};

@NgModule({
  imports: [RouterModule.forRoot(routes, config)],
  exports: [RouterModule],
})
export class AppRoutingModule {
}
