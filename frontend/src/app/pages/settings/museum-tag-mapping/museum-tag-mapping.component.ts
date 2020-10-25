import { Component, OnInit } from '@angular/core';
import {LocalDataSource} from 'ng2-smart-table';
import {DataAccessService} from '../../../services/data-access.service';
import {TopicDropDownComponent} from "../../util/topic-drop-down/topic-drop-down.component";
import {CellDropDownComponent} from "../../util/cell-drop-down/cell-drop-down.component";

@Component({
  selector: 'ngx-museum-tag-mapping',
  templateUrl: './museum-tag-mapping.component.html',
  styleUrls: ['./museum-tag-mapping.component.scss'],
})
export class MuseumTagMappingComponent implements OnInit {
  selectedMuseum: any;
  museums = ['The Metropolitan Museum of Art', 'Rijksmuseum Amsterdam', 'Cleveland Museum of Art'];
  mm = {'The Metropolitan Museum of Art': 1, 'Rijksmuseum Amsterdam': 2, 'Cleveland Museum of Art': 3};
  constructor(private dataAccess: DataAccessService) { }

  ngOnInit() {
    this.dataAccess.getMuseumTagMapping().subscribe(res => {
      this.loading = false;
      this.source.load(res.data);
    });
  }


  settings = {
    pager: {
      display: true,
      perPage: 50,
    },
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
      tagName: {
        title: 'Canonical Tag',
        type: 'string',
        editable: false,
      },
      tagMap: {
        title: 'Museum Tag',
        type: 'html',
        editor: {
          type: 'custom',
          valuePrepareFunction: (cell, row) => row,
          component: CellDropDownComponent,
        },
      },
      displayName: {
        title: 'Source Museum',
        type: 'string',
        editable: false,
      },
    },
  };

  source: LocalDataSource = new LocalDataSource();
  museumSampleData={};
  loading = true;



  onEditConfirm(event) {
    console.log(event.data);
    console.log(event.newData);

    this.dataAccess.updateTagMapping(event.data.mapId[0], event.newData.tagMap).subscribe(res => {
      event.confirm.resolve();
    });
  }

  getMapping(event) {
    this.museumSampleData = {};
    console.log(this.mm[event])
    const v = this.mm[event];
    this.source.setFilter([{ field: 'displayName', search: event}])
    this.dataAccess.getSampleMetaData(v).subscribe(res => {
      this.museumSampleData = res;

      const flatten = (objectOrArray, prefix = '') => {
        const nestElement = (prev, value, key) => (value
        && typeof value === 'object'
          ? { ...prev, ...flatten(value, `${prefix}${key}.`) }
          : { ...prev, ...{ [`${prefix}${key}`]: value } });

        return Array.isArray(objectOrArray)
          ? objectOrArray.reduce(nestElement, {})
          : Object.keys(objectOrArray).reduce(
            (prev, element) => nestElement(prev, objectOrArray[element], element),
            {},
          );
      };

      const a = flatten(res);
      console.log(Object.keys(a));
      this.dataAccess.changeSampleTags(Object.keys(a));

    });

  }

  clicked(event) {
    console.log(event);
  }
}
