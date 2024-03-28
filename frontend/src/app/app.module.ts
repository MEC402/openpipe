/**
 * @license
 * Copyright Akveo. All Rights Reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 */
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { ThemeModule } from './@theme/theme.module';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import {
  NbButtonModule,
  NbCardModule,
  NbChatModule,
  NbDatepickerModule,
  NbDialogModule, NbLayoutModule,
  NbMenuModule,
  NbSidebarModule,
  NbToastrModule,
  NbWindowModule,
} from '@nebular/theme';
import {NbAuthModule, NbOAuth2AuthStrategy, NbOAuth2ResponseType} from '@nebular/auth';
import { OAuth2LoginComponent } from './oauth2-login/oauth2-login.component';
import { OAuth2CallbackComponent } from './oauth2-callback/oauth2-callback.component';

@NgModule({
  declarations: [AppComponent, OAuth2LoginComponent, OAuth2CallbackComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,

    ThemeModule.forRoot(),

    NbSidebarModule.forRoot(),
    NbMenuModule.forRoot(),
    NbDatepickerModule.forRoot(),
    NbDialogModule.forRoot(),
    NbWindowModule.forRoot(),
    NbToastrModule.forRoot(),
    NbChatModule.forRoot({
      messageGoogleMapKey: 'AIzaSyA_wNuCzia92MAmdLRzmqitRGvCF7wCZPY',
    }),
    NbAuthModule.forRoot({
      strategies: [
        NbOAuth2AuthStrategy.setup({
          clientId: '222308801855-00ija7jbfffolbrsuo54qoake8uld3um.apps.googleusercontent.com',
          name: 'google',
          authorize: {
            endpoint: 'https://accounts.google.com/o/oauth2/v2/auth',
            responseType: NbOAuth2ResponseType.TOKEN,
            scope: 'https://www.googleapis.com/auth/userinfo.profile',
            redirectUri: 'http://d5bnzen7zsmwo.cloudfront.net/auth/callback',
            //redirectUri: 'http://localhost:4200/auth/callback',
          },
        }),
      ],
    }),
    NbLayoutModule,
    NbCardModule,
    NbButtonModule,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {
}
