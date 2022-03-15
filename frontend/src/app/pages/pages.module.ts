import { NgModule } from '@angular/core';
import {
    NbAccordionModule, NbActionsModule, NbBadgeModule,
    NbButtonModule,
    NbCardModule, NbChatModule,
    NbCheckboxModule, NbContextMenuModule, NbDatepickerModule,
    NbDialogRef,
    NbIconModule,
    NbInputModule, NbLayoutModule,
    NbListModule,
    NbMenuModule,
    NbPopoverModule,
    NbRadioModule,
    NbSelectModule, NbSidebarModule, NbSpinnerModule,
    NbStepperModule,
    NbTabsetModule,
    NbToggleModule,
    NbUserModule,
} from '@nebular/theme';

import { ThemeModule } from '../@theme/theme.module';
import { PagesComponent } from './pages.component';
import { PagesRoutingModule } from './pages-routing.module';
import { MiscellaneousModule } from './miscellaneous/miscellaneous.module';
import {ButtonViewComponent, HomeComponent} from './home/home.component';
import { CollectionsComponent } from './collections/collections.component';
import { SettingsComponent } from './settings/settings.component';
import { CardComponent } from './util/card/card.component';
import { CardDeckComponent } from './util/card-deck/card-deck.component';


import {MatPaginatorModule} from '@angular/material/paginator';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {FormsModule} from '@angular/forms';
import {Ng2SmartTableModule} from 'ng2-smart-table';
import { MetadataSelectorComponent } from './util/metadata-selector/metadata-selector.component';
import { PreviewCardComponent } from './util/preview-card/preview-card.component';
import { CanonicalMetaTagsComponent } from './settings/canonical-meta-tags/canonical-meta-tags.component';
import { MetaTagEditorComponent } from './settings/meta-tag-editor/meta-tag-editor.component';
import { UploaderComponent } from './uploader/uploader.component';
import {FileUploadModule} from 'ng2-file-upload';
import { AssetsComponent } from './assets/assets.component';
import { ReportsComponent } from './reports/reports.component';
import {ServiceStatusComponent} from './reports/service-status/service-status.component';
import {MissingImagesComponent} from './reports/missing-images/missing-images.component';
import {AssetDefectsReportComponent} from './reports/asset-defects-report/asset-defects-report.component';
import {AssetChangesComponent} from './reports/asset-changes/asset-changes.component';
import {DragDropModule} from '@angular/cdk/drag-drop';
import { LayoutEditorComponent } from './layout-editor/layout-editor.component';
import { DocsComponent } from './docs/docs.component';
import {KonvaModule} from 'ng2-konva';
import { FolderCardComponent } from './util/folder-card/folder-card.component';
import {HttpClient, HttpClientModule} from '@angular/common/http';
import { DsAppSettingsComponent } from './settings/ds-app-settings/ds-app-settings.component';
import { ChatbotComponent } from './chatbot/chatbot.component';
import { TopicDropDownComponent } from './util/topic-drop-down/topic-drop-down.component';
import { MuseumTagMappingComponent } from './settings/museum-tag-mapping/museum-tag-mapping.component';
import {NgxJsonViewerModule} from "ngx-json-viewer";
import { CellDropDownComponent } from './util/cell-drop-down/cell-drop-down.component';
import { CanvasEditorComponent } from './layout-editor/canvas-editor/canvas-editor.component';
import { AssetComponent } from './asset/asset.component';
import { TopicsComponent } from './topics/topics.component';
import { TopicInfoComponent } from './topics/topic-info/topic-info.component';


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
        NbLayoutModule,
        NbContextMenuModule,
        NbDatepickerModule,
        DragDropModule,
        NbActionsModule,
        NbSidebarModule,
        KonvaModule,
        HttpClientModule,
        NbSpinnerModule,
        NbChatModule,
        NgxJsonViewerModule,
        NbBadgeModule,
    ],
  entryComponents: [ButtonViewComponent, TopicDropDownComponent, CellDropDownComponent],
  declarations: [
    ButtonViewComponent,
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
    ReportsComponent,
    ServiceStatusComponent,
    MissingImagesComponent,
    AssetDefectsReportComponent,
    AssetChangesComponent,
    LayoutEditorComponent,
    DocsComponent,
    FolderCardComponent,
    DsAppSettingsComponent,
    ChatbotComponent,
    TopicDropDownComponent,
    MuseumTagMappingComponent,
    CellDropDownComponent,
    CanvasEditorComponent,
    AssetComponent,
    TopicsComponent,
    TopicInfoComponent,
  ],
})
export class PagesModule {
}
