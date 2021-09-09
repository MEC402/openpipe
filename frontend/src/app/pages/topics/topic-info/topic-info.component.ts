import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {DataAccessService} from '../../../services/data-access.service';
import {takeUntil} from 'rxjs/operators';
import {Observable, Subject} from 'rxjs';

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

  constructor(private dataAccess: DataAccessService) {

  }

  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }


  ngOnInit() {
    this.dataAccess.getTopicByCode(this.topicCode, 1, this.pageSize).
    pipe(takeUntil(this._destroyed$)).subscribe(res => {
      const pages = Array.from(Array(Math.ceil(res.total / this.pageSize)).keys());
      this.topicData = res.data;
      console.log(this.topicData);
    });
  }

  saveChanges() {
    console.log("save")
  }

  showAliases(aliases) {
    this.selectedTopicAliases=aliases;
  }
}
