import {Component, Input, OnDestroy, OnInit, TemplateRef} from '@angular/core';
import {DataAccessService} from '../../../services/data-access.service';
import {takeUntil} from 'rxjs/operators';
import {Observable, Subject} from 'rxjs';
import {NbDialogRef, NbDialogService} from '@nebular/theme';

@Component({
  selector: 'ngx-topic-info',
  templateUrl: './topic-info.component.html',
  styleUrls: ['./topic-info.component.scss'],
})
export class TopicInfoComponent implements OnInit, OnDestroy {
  @Input() topicCode;
  @Input() topicType;
  pageSize = 25;
  topicData;
  selectedTopicAliases;
  private _destroyed$ = new Subject();
  aliasData = [];
  topicPage = 1;
  aliasPage = 1;
  totalTopicPages = 1;
  totalAliasPages = 1;
  selectedTopic;
  topicMergeList = [];
  selectedTopicList = [];
  mergeName = '';
  aliasToggleMerge = 0; // 0 is dont show - 1 is aliases - 2 is merge card
  searchTerm = '';
  searchMode = false;

  constructor(private dataAccess: DataAccessService,
              private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>) {

  }

  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }


  ngOnInit() {
    this.aliasToggleMerge = 0;
    this.topicPage = 1;
    this.searchMode = false;
    this.dataAccess.getTopicByCode(this.topicCode, this.topicPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalTopicPages = Math.ceil(res.total / this.pageSize);
      this.topicData = res.data;
      console.log(this.topicData);
    });
  }

  saveChanges(topicIn) {
    console.log(topicIn);
    this.dataAccess.updateTopic(topicIn.topicId, {'name' : topicIn.topicName}).subscribe(res => {
      console.log(res);
    });
  }

  showAliases(topic) {
    this.selectedTopicAliases = [];
    this.aliasToggleMerge = 1;
    this.selectedTopic = topic;
    this.dataAccess.getTopicAliases(topic.topicId, this.aliasPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalAliasPages = Math.ceil(res.total / this.pageSize);
      this.selectedTopicAliases = res.data;
      console.log(this.selectedTopicAliases);
    });
  }

  setAsTopicRepresentative(asset) {
    this.dataAccess.updateTopic(this.selectedTopic.topicId, {'repMetaDataId' : asset.metaDataId}).subscribe(res => {
      this.selectedTopic.repImage = asset.image;
      console.log(res);
    });
  }

  prevTopicPage() {
    this.topicPage--;
    if (this.searchMode) {
      this.dataAccess.searchTopic(this.searchTerm, this.topicCode, this.topicPage, this.pageSize).
      pipe(takeUntil(this._destroyed$)).subscribe(res => {
        this.totalTopicPages = Math.ceil(res.total / this.pageSize);
        this.topicData = res.data;
        console.log(this.topicData);
      });
    } else {
      this.dataAccess.getTopicByCode(this.topicCode, this.topicPage, this.pageSize).
      pipe(takeUntil(this._destroyed$)).subscribe(res => {
        this.totalTopicPages = Math.ceil(res.total / this.pageSize);
        this.topicData = res.data;
        console.log(this.topicData);
      });
    }
  }

  nextTopicPage() {
    this.topicPage++;
    if (this.searchMode) {
      this.dataAccess.searchTopic(this.searchTerm, this.topicCode, this.topicPage, this.pageSize).
      pipe(takeUntil(this._destroyed$)).subscribe(res => {
        this.totalTopicPages = Math.ceil(res.total / this.pageSize);
        this.topicData = res.data;
        console.log(this.topicData);
      });
    } else {
      this.dataAccess.getTopicByCode(this.topicCode, this.topicPage, this.pageSize).
      pipe(takeUntil(this._destroyed$)).subscribe(res => {
        this.totalTopicPages = Math.ceil(res.total / this.pageSize);
        this.topicData = res.data;
        console.log(this.topicData);
      });
    }

  }

  prevAliasPage() {
    this.aliasPage--;
    this.dataAccess.getTopicAliases(this.selectedTopic.topicId, this.aliasPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalAliasPages = Math.ceil(res.total / this.pageSize);
      this.selectedTopicAliases = res.data;
      console.log(this.selectedTopicAliases);
    });
  }

  nextAliasPage() {
    this.aliasPage++;
    this.dataAccess.getTopicAliases(this.selectedTopic.topicId, this.aliasPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalAliasPages = Math.ceil(res.total / this.pageSize);
      this.selectedTopicAliases = res.data;
      console.log(this.selectedTopicAliases);
    });
  }

  addToMergeList(t) {
    if (!this.topicMergeList.includes(t)) {
      t['selected'] = false;
      this.topicMergeList.push(t);
    }
  }

  openMerge() {
    this.aliasToggleMerge = 2;
  }

  toggle(topic , checked) {
    console.log(topic)
    if ( checked ) {
      this.selectedTopicList.push(topic.topicId);
    } else {
      const index = this.selectedTopicList.indexOf(topic.topicId);
      if (index > -1) {
        this.selectedTopicList.splice(index, 1);
      }
    }
  }

  close() {
    this.aliasToggleMerge = 0;
  }

  mergeTopics() {
    console.log(this.selectedTopicList);
    console.log(this.topicMergeList);
    this.topicMergeList =  this.topicMergeList.filter( ( d ) => !this.selectedTopicList.includes( d.topicId ) );
    this.topicData =  this.topicData.filter( ( d ) => !this.selectedTopicList.includes( d.topicId ) );

    const mergeData = {
      'name': this.mergeName,
      'code': this.topicCode,
      'type': this.topicType,
      'mergeTopicIds': this.selectedTopicList,
    };

    this.dataAccess.mergeTopics(mergeData).subscribe( res => {
      console.log(res);
      res['selected'] = false;
      this.topicData.push(res);
      this.selectedTopicList = [];
      this.mergeName = '';
    });


  }

  selectAll() {
    this.topicMergeList.forEach(d => {
      d.selected = true;
      this.selectedTopicList.push(d.topicId);
    });
  }

  deselectAll() {
    this.topicMergeList.forEach(d => {
      d.selected = false;
    });
    this.selectedTopicList = [];
  }

  searchTopicTerm() {
    if (this.searchTerm.trim().length > 0) {
      this.topicPage = 1;
      this.aliasToggleMerge = 0;
      this.searchMode = true;
      this.dataAccess.searchTopic(this.searchTerm, this.topicCode, 1, 25).
      pipe(takeUntil(this._destroyed$)).subscribe(res => {
        this.totalTopicPages = Math.ceil(res.total / this.pageSize);
        this.topicData = res.data;
        console.log(this.topicData);
      });
    }
  }

  showAllResults() {
    this.aliasToggleMerge = 0;
    this.topicPage = 1;
    this.searchMode = false;
    this.dataAccess.getTopicByCode(this.topicCode, this.topicPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalTopicPages = Math.ceil(res.total / this.pageSize);
      this.topicData = res.data;
      console.log(this.topicData);
    });
  }
}

