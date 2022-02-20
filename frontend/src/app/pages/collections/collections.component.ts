import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {DataAccessService} from '../../services/data-access.service';
import {NbPopoverDirective} from '@nebular/theme';
import {Observable, Subject} from 'rxjs';
import {Router} from '@angular/router';


@Component({
  selector: 'ngx-collections',
  templateUrl: './collections.component.html',
  styleUrls: ['./collections.component.scss'],
})
export class CollectionsComponent implements OnInit, OnDestroy {
  protected destroy$ = new Subject<void>();

  collections = [];
  assets = [];
  currentFolder = {'name': ['test'], 'id': [-1]};
  metaTags: any;
  newCollectionName;
  @ViewChild(NbPopoverDirective, { static: false }) popover: NbPopoverDirective;

  constructor(private dataAccess: DataAccessService, private router: Router) {
    dataAccess.getFolders(1, 200).subscribe(res => {
      console.log(res.data);
      this.collections = res.data;
    });

  }

  private _destroyed$ = new Subject();

  ngOnDestroy(): void {
    this._destroyed$.next();
    this._destroyed$.complete();
  }

  ngOnInit() {
    this.dataAccess.getCanonicalMetaTags().subscribe(d => {
      this.dataAccess.changeMessage(d);
    });

  }

  onFolderOpenClick(element) {
    this.router.navigateByUrl('/pages/folder/' + element.id, {state:{data:element}});
  }

  onFolderDeleteClick(c) {
    this.dataAccess.deleteFolder(c.id[0]);
    for ( let i = 0; i < this.collections.length; i++) {
      if ( this.collections[i].id[0] === c.id[0]) {
        this.collections.splice(i, 1);
        break;
      }
    }
  }

  onCreateCollection() {
    this.popover.hide();
    this.dataAccess.createCollection(this.newCollectionName).subscribe(res0 => {
      this.dataAccess.getCollections().subscribe(res => {
          this.collections = res.data;
      });
    });
  }

  goToMergePage() {
    this.router.navigateByUrl('/pages/moveAssets');
  }
}

