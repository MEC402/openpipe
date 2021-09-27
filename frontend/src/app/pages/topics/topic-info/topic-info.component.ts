import {Component, Input, OnDestroy, OnInit, TemplateRef} from '@angular/core';
import {DataAccessService} from '../../../services/data-access.service';
import {takeUntil} from 'rxjs/operators';
import {Observable, Subject} from 'rxjs';
import {NbDialogRef, NbDialogService} from "@nebular/theme";

@Component({
  selector: 'ngx-topic-info',
  templateUrl: './topic-info.component.html',
  styleUrls: ['./topic-info.component.scss'],
})
export class TopicInfoComponent implements OnInit, OnDestroy {
  @Input() topicCode;
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
  mergeName: any;

  constructor(private dataAccess: DataAccessService,
              private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>) {

  }

  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }


  ngOnInit() {
    this.dataAccess.getTopicByCode(this.topicCode, this.topicPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalTopicPages = Math.ceil(res.total / this.pageSize);
      this.topicData = res.data;
      console.log(this.topicData);
    });
  }

  saveChanges(topicIn) {
    console.log(topicIn);
    this.dataAccess.updateTopic(topicIn.topicId, topicIn.topicName).subscribe(res => {
      console.log(res);
    });
  }

  showAliases(topic) {
    this.selectedTopic = topic;
    this.dataAccess.getTopicAliases(topic.topicId, this.aliasPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalAliasPages = Math.ceil(res.total / this.pageSize);
      this.selectedTopicAliases = res.data;
      console.log(this.selectedTopicAliases);
    });
  }

  setAsTopicRepresentative(metaDataId: any) {

  }

  prevTopicPage() {
    this.topicPage--;
    this.dataAccess.getTopicByCode(this.topicCode, this.topicPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalTopicPages = Math.ceil(res.total / this.pageSize);
      this.topicData = res.data;
      console.log(this.topicData);
    });
  }

  nextTopicPage() {
    this.topicPage++;
    this.dataAccess.getTopicByCode(this.topicCode, this.topicPage, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      this.totalTopicPages = Math.ceil(res.total / this.pageSize);
      this.topicData = res.data;
      console.log(this.topicData);
    });
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
    this.topicMergeList.push(t);
  }

  openDialog(dialog: TemplateRef<any>) {

    this.dialogRef = this.dialogService.open(dialog, { context: this.topicMergeList });
  }

  toggle(topic,event) {
    console.log(topic)
    console.log(event)

  }
}
