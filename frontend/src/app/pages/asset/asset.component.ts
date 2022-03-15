import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {DataAccessService} from "../../services/data-access.service";

@Component({
  selector: 'ngx-asset',
  templateUrl: './asset.component.html',
  styleUrls: ['./asset.component.scss']
})
export class AssetComponent implements OnInit {
  private metaDataId: string;
  assetVerified: any;
  assetName: any;
  assetScore: any;
  assetAccessStatus: any;
  assetLink: any;
  selectedAssetMetaTag: any;
  assetImage: any;
  selectedAssetChanges: {};
  selectTagNames = ['openpipe_canonical_artist', 'openpipe_canonical_title',  'openpipe_canonical_displayDate' , 'openpipe_canonical_date',
    'openpipe_canonical_Moment', 'openpipe_canonical_medium', 'openpipe_canonical_Technique', 'openpipe_canonical_country'
    , 'openpipe_canonical_culture', 'openpipe_canonical_period', 'openpipe_canonical_biography'
    , 'openpipe_canonical_longitude', 'openpipe_canonical_latitude', 'openpipe_canonical_classification',
    'openpipe_canonical_Object_Type', 'openpipe_canonical_Region', 'openpipe_canonical_largeImageDimensions'];
  private currentAsset: any;
  allTagsView = false;

  constructor(private route: ActivatedRoute, private dataAccess: DataAccessService) {}

  ngOnInit() {
    this.metaDataId = this.route.snapshot.paramMap.get('mid');
    this.dataAccess.getAssetByMetaDataId(this.metaDataId).subscribe(res => {
      this.fillForm(res.tagData);
    });
  }

  fillForm(data) {
    console.log(data);
    this.currentAsset = data;
    this.assetName = data.openpipe_canonical_title;
    this.assetImage = data.openpipe_canonical_largeImage;
    // this.assetVerified = data.assetVerified;
    // this.assetScore = data.assetScore;
    this.assetAccessStatus = true;
    this.selectedAssetChanges = {};
    const s = data.openpipe_canonical_source;

    if (s.includes('Metropolitan')) {
      this.assetLink = 'https://www.metmuseum.org/art/collection/search/' + data.objectID;
    } else if (s.includes('Cleveland')) {
      this.assetLink = 'https://www.clevelandart.org/art/' + data.accession_number;
    } else {
      this.assetLink = 'Link not available';
    }

    console.log(data);
    const temp = [];
    for (const [key, value] of Object.entries(data)) {
      if (this.selectTagNames.includes(key))
        temp.push({'tagName': key.split('_')[2], 'value': value, 'originalTagName': key});
    }
    this.selectedAssetMetaTag = temp;
  }

  sendTheNewValue($event: Event) {

  }

  saveAssetChanges() {

  }

  showAllTags() {
    const temp = [];
    if (!this.allTagsView){
      this.allTagsView = true;
      for (const [key, value] of Object.entries(this.currentAsset)) {
        temp.push({'tagName': key, 'value': value, 'originalTagName': key});
      }
    } else {
      this.allTagsView = false;
      for (const [key, value] of Object.entries(this.currentAsset)) {
        if (this.selectTagNames.includes(key))
          temp.push({'tagName': key.split('_')[2], 'value': value, 'originalTagName': key});
      }
    }
    this.selectedAssetMetaTag = temp;
  }
}
