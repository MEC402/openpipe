import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { PagesComponent } from './pages.component';
import { NotFoundComponent } from './miscellaneous/not-found/not-found.component';
import {HomeComponent} from './home/home.component';
import {CollectionsComponent} from './collections/collections.component';
import {SettingsComponent} from './settings/settings.component';
import {UploaderComponent} from './uploader/uploader.component';
import {AssetsComponent} from './assets/assets.component';
import {ReportsComponent} from './reports/reports.component';
import {DocsComponent} from './docs/docs.component';
import {LayoutEditorComponent} from './layout-editor/layout-editor.component';
import {ChatbotComponent} from './chatbot/chatbot.component';
import {AssetComponent} from './asset/asset.component';
import {TopicsComponent} from './topics/topics.component';
import {MoveAssetsComponent} from "./collections/move-assets/move-assets.component";
import {FolderContentComponent} from "./collections/folder-content/folder-content.component";
import {SyncComponent} from "./sync/sync.component";

const routes: Routes = [{
  path: '',
  component: PagesComponent,
  children: [
    {
      path: 'home',
      component: HomeComponent,
    },
    {
      path: 'asset/:mid',
      component: AssetComponent,
    },
    {
      path: 'topics',
      component: TopicsComponent,
    },
    {
      path: 'collections',
      component: CollectionsComponent,
    },
    {
      path: 'folder/:fid',
      component: FolderContentComponent,
    },
    {
      path: 'assets',
      component: AssetsComponent,
    },
    {
      path: 'settings',
      component: SettingsComponent,
    },
    {
      path: 'sync',
      component: SyncComponent,
    },
    {
      path: 'layoutEditor',
      component: LayoutEditorComponent,
    },
    {
      path: 'uploader',
      component: UploaderComponent,
    },
    {
      path: 'reports',
      component: ReportsComponent,
    },
    {
      path: 'chatbot',
      component: ChatbotComponent,
    },
    {
      path: 'docs',
      component: DocsComponent,
    },
    {
      path: 'moveAssets',
      component: MoveAssetsComponent,
    },
    {
      path: 'miscellaneous',
      loadChildren: () => import('./miscellaneous/miscellaneous.module')
        .then(m => m.MiscellaneousModule),
    },
    {
      path: '',
      redirectTo: 'home',
      pathMatch: 'full',
    },
    {
      path: '**',
      component: NotFoundComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PagesRoutingModule {
}
