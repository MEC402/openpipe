import { NgModule } from '@angular/core';
import {
  NbAccordionModule,
  NbButtonModule,
  NbCardModule,
  NbCheckboxModule,
  NbDialogRef,
  NbIconModule,
  NbInputModule,
  NbListModule,
  NbMenuModule,
  NbPopoverModule,
  NbRadioModule,
  NbSelectModule,
  NbStepperModule,
  NbTabsetModule,
  NbToggleModule,
  NbUserModule
} from '@nebular/theme';

import { ThemeModule } from '../@theme/theme.module';
import { PagesComponent } from './pages.component';
import { PagesRoutingModule } from './pages-routing.module';
import { MiscellaneousModule } from './miscellaneous/miscellaneous.module';
import { HomeComponent } from './home/home.component';
import { CollectionsComponent } from './collections/collections.component';
import { SettingsComponent } from './settings/settings.component';
import { CardComponent } from './util/card/card.component';
import { CardDeckComponent } from './util/card-deck/card-deck.component';


import {MatPaginatorModule} from '@angular/material/paginator';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {FormsModule} from "@angular/forms";
import {Ng2SmartTableModule} from "ng2-smart-table";
import { MetadataSelectorComponent } from './util/metadata-selector/metadata-selector.component';
import { PreviewCardComponent } from './util/preview-card/preview-card.component';
import { CanonicalMetaTagsComponent } from './settings/canonical-meta-tags/canonical-meta-tags.component';
import { MetaTagEditorComponent } from './settings/meta-tag-editor/meta-tag-editor.component';
import { UploaderComponent } from './uploader/uploader.component';
import {FileUploadModule} from "ng2-file-upload";
import { AssetsComponent } from './assets/assets.component';

@NgModule({
  providers: [
    { provide: NbDialogRef, useValue: {} },

  ],
  imports: [
    PagesRoutingModule,
    ThemeModule,
    NbMenuModule,
    MiscellaneousModule,
    NbCardModule,
    NbButtonModule,
    NbInputModule,
    // material
    MatPaginatorModule,
    MatCardModule,
    MatButtonModule,
    NbIconModule,
    FormsModule,
    NbCheckboxModule,
    Ng2SmartTableModule,
    NbListModule,
    NbPopoverModule,
    NbStepperModule,
    NbToggleModule,
    NbRadioModule,
    NbTabsetModule,
    NbAccordionModule,
    NbUserModule,
    FileUploadModule,
    NbSelectModule,

  ],
  declarations: [
    PagesComponent,
    HomeComponent,
    CollectionsComponent,
    SettingsComponent,
    CardComponent,
    CardDeckComponent,
    MetadataSelectorComponent,
    PreviewCardComponent,
    CanonicalMetaTagsComponent,
    MetaTagEditorComponent,
    UploaderComponent,
    AssetsComponent,
  ],
})
export class PagesModule {
}
