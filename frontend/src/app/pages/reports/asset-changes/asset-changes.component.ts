import {Component, ElementRef, HostListener, OnInit} from '@angular/core';
import {LocalDataSource} from "ng2-smart-table";
import {DataAccessService} from "../../../services/data-access.service";

@Component({
  selector: 'ngx-asset-changes',
  templateUrl: './asset-changes.component.html',
  styleUrls: ['./asset-changes.component.scss']
})
export class AssetChangesComponent implements OnInit {
  ngOnInit() {
  }

  settings = {
    actions: {
      add: false,
      delete: false,
    },
    edit: {
      editButtonContent: '<i class="nb-edit"></i>',
      saveButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmSave : true,
    },
    columns: {
      shortName: {
        title: 'Asset Name',
        type: 'string',
        editable: false,
      },
      tagName: {
        title: 'Tag Name',
        type: 'string',
        editable: false,
      },
      value: {
        title: 'value',
        type: 'string',
      },
      sourceName: {
        title: 'Source Museum',
        type: 'string',
        editable: false,
      },
    },
  };

  source: LocalDataSource = new LocalDataSource();

  constructor(private dataAccess: DataAccessService,private el: ElementRef) {
    dataAccess.getAssetsMissingImageReport().subscribe(res => {
      console.log(res)
      this.source.load(res.data);
    });
  }


  onEditConfirm(event) {
    console.log('edit');
    this.dataAccess.updateCanonicalMetaTag(event.data.id, event.newData.name);
    event.confirm.resolve();
  }

  @HostListener('click') onMouseClick() {
    console.log('clicked');
    this.highlight('blue');
  }

  private highlight(color: string) {
    console.log(this.el.nativeElement)
    this.el.nativeElement.style.backgroundColor = color;
  }
}
