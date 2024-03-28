import {Component, OnInit, TemplateRef} from '@angular/core';
import {NbDialogRef, NbDialogService} from '@nebular/theme';
import {DataAccessService} from '../../services/data-access.service';

@Component({
  selector: 'ngx-sync',
  templateUrl: './sync.component.html',
  styleUrls: ['./sync.component.scss'],
})
export class SyncComponent implements OnInit {

  constructor(private dialogService: NbDialogService,
              protected dialogRef: NbDialogRef<any>,
              private dataAccess: DataAccessService) {
  }

  currentSyncStatus;
  running;
  countActionsComplete;
  countActionsTotal;
  lastRun;
  ready;
  action;
  startTime;
  runTime;
  complete;
  results;
  script;
  progressPercentage = 0;

  ngOnInit() {
    this.ShowSyncStatus();
  }

  ShowSyncStatus() {
    this.dataAccess.getSyncStatus().subscribe(d => {
      const data = d.status.data;
      if ('next' in data) {
        this.currentSyncStatus = 'ready';
      } else {
        this.currentSyncStatus = 'running';
        this.running = data.running;
        this.lastRun = data.lastRun;
        this.ready = data.ready;
        this.action = data.action;
        this.startTime = data.startTime;
        this.runTime = data.runTime;
        this.complete = data.complete;
        this.results = data.results;
        this.script = data.script;
        this.countActionsComplete = data.countActionsComplete;
        this.countActionsTotal = data.countActionsTotal;
        this.progressPercentage = (this.countActionsComplete / this.countActionsTotal) * 100;
      }

    });
  }

  runSync(dialog: TemplateRef<any>) {
    this.dialogRef = this.dialogService.open(dialog, {context: 'data', hasBackdrop: true});
  }

  confirmRun() {
    console.log('runSync');
    this.dialogRef.close();
    this.dataAccess.runSync().subscribe(d => {

    });
  }
}
