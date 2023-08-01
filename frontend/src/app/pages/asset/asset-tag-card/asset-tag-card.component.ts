import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {DataAccessService} from '../../../services/data-access.service';
import {log} from "util";

@Component({
  selector: 'ngx-asset-tag-card',
  templateUrl: './asset-tag-card.component.html',
  styleUrls: ['./asset-tag-card.component.scss'],
})
export class AssetTagCardComponent implements OnInit {
  @Input() asset;


  currentAssetName: any;
  currentAssetVerified = false;
  currentAssetLink: string;
  currentAssetScore: number;
  currentAssetType: string;
  currentAssetFullImage;
  tombstoneTags = [];
  canonicalTags = [];
  museumTags = [];
  selectedAssetChanges = {};
  currentAssetImage: any;
  currentAssetAccessStatus = true;
  newTagCounter = 0;

  selectTagNames = ['openpipe_canonical_artist', 'openpipe_canonical_title',  'openpipe_canonical_displayDate' ,
    'openpipe_canonical_Moment', 'openpipe_canonical_medium', 'openpipe_canonical_Technique', 'openpipe_canonical_country'
    , 'openpipe_canonical_culture', 'openpipe_canonical_period', 'openpipe_canonical_biography'
    , 'openpipe_canonical_longitude', 'openpipe_canonical_latitude', 'openpipe_canonical_classification',
    'openpipe_canonical_Object_Type', 'openpipe_canonical_Region', 'openpipe_canonical_largeImageDimensions','openpipe_canonical_source'];

  constructor(private dataAccess: DataAccessService) { }

  ngOnInit() {
    this.newTagCounter=0;
  }

  updateUI(a) {
    this.asset = a;
    this.currentAssetName = this.asset.openpipe_canonical_title[0];
    this.currentAssetVerified = this.asset.assetVerified[0];
    this.currentAssetScore = this.asset.assetScore;
    this.currentAssetType = this.asset.assetType;
    this.currentAssetImage = this.asset.openpipe_canonical_smallImage[0];
    this.currentAssetFullImage = this.asset.openpipe_canonical_fullImage[0];
    this.currentAssetAccessStatus = true;
    this.selectedAssetChanges = {};
    let s = 'Local';
    if ('openpipe_canonical_source' in this.asset) {
      s = this.asset.openpipe_canonical_source[0][Object.keys(this.asset.openpipe_canonical_source[0])[0]];
    }

    if (s.includes('Metropolitan')) {
      this.currentAssetLink = 'https://www.metmuseum.org/art/collection/search/' +this.asset.objectID[0][Object.keys(this.asset.objectID[0])[0]];
    } else if (s.includes('Cleveland')) {
      this.currentAssetLink = 'https://www.clevelandart.org/art/' + this.asset.accession_number[0][Object.keys(this.asset.accession_number[0])[0]]
      ;
    } else if (s.includes('Rijks')) {
      this.currentAssetLink = 'https://www.rijksmuseum.nl/en/collection/' + this.asset.objectNumber[0][Object.keys(this.asset.objectNumber[0])[0]]
      ;
    } else {
      this.currentAssetLink = 'Link not available';
    }

    this.separateTagsInGroups();
    console.log(this.tombstoneTags);
    console.log(this.canonicalTags)
  }

  saveAssetChanges() {
    this.dataAccess.saveAssetChanges(this.asset.metaDataId, this.selectedAssetChanges).subscribe(res => {
      console.log(res);
    });
  }

  saveMetaTagChanges() {
    this.dataAccess.saveMetaTagChanges(this.asset.metaDataId, this.selectedAssetChanges).subscribe(res => {
      console.log(res);
    });
  }

  sendTheNewValue(e, metaTagId,tagName) {
    const value = e;
    console.log(value)
    console.log(metaTagId)
    this.selectedAssetChanges[metaTagId] = value;
    console.log(this.selectedAssetChanges)
  }

  onTabChange() {
    this.separateTagsInGroups();
    this.selectedAssetChanges={};
  }

  separateTagsInGroups() {
    const ts = [];
    const ct = [];
    const mt = [];

    console.log(this.asset)

    for (const [key, value] of Object.entries(this.asset)) {
      if (this.selectTagNames.includes(key)) {
        let displayKey = key.split('_')[2];
        ts.push({'tagName': displayKey, 'value': value, 'originalTagName': key});
        ct.push({'tagName': displayKey, 'value': value, 'originalTagName': key});
      } else if (key.includes('openpipe_canonical_'))
        ct.push({'tagName': key.split('_')[2], 'value': value, 'originalTagName': key});
      else
        mt.push({'tagName': key, 'value': value, 'originalTagName': key});

    }

    this.tombstoneTags = ts;
    this.canonicalTags = ct;
    this.museumTags = mt;
  }

  addNewElement(container: HTMLElement, originalTagName) {
    const textBox = document.createElement('textarea');
    textBox.classList.add('form-control');
    textBox.id = "New_tag:"+ originalTagName + ":" + this.newTagCounter;
    this.newTagCounter++;
    textBox.addEventListener('input', (e) => this.sendTheNewValue((e.target as HTMLButtonElement).value,textBox.id,originalTagName ));
    container.appendChild(textBox);
  }

  isArray(obj : any ) {
    return Array.isArray(obj)
  }

  getFirstValue(tag: any) {
    return tag[0][Object.keys(tag[0])[0]]
  }
  getDictValue(v: any) {
    return v[Object.keys(v)[0]]
  }

  getDictKey(k: any) {
    return Object.keys(k)[0];
  }
}
