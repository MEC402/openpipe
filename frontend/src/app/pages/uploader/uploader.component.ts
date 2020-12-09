import {Component , OnInit } from '@angular/core';
import {FileUploader , FileItem } from 'ng2-file-upload';
import {DataAccessService } from '../../services/data-access.service';
import {HttpEventType, HttpResponse} from "@angular/common/http";

//tslint:disable

// const URL = '/api/';
const URL = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/addUserAssets.py';

@ Component ({
  selector : 'ngx-uploader',
  templateUrl : './uploader.component.html',
  styleUrls : ['./uploader.component.scss']
})
export class UploaderComponent  {
  public uploader;
  public hasBaseDropZoneOver : boolean = false;
  public hasAnotherDropZoneOver : boolean = false;
  response:string;

  collections = [];
  chosenCollection={"id":-1};

  constructor(private dataAccess : DataAccessService ) {
    this.uploader = new FileUploader({
      formatDataFunctionIsAsync: true,
      formatDataFunction: async (item) => {
        return new Promise( (resolve, reject) => {
          resolve({
            name: item._file.name,
            length: item._file.size,
            contentType: item._file.type,
            status:item._status,
            date: new Date()
          });
        });
      }
    });

    this.hasBaseDropZoneOver = false;
    this.hasAnotherDropZoneOver = false;

    this.response = '';

    this.uploader.response.subscribe( res => this.response = res );
  }

  ngOnInit() {
    this.uploader.uploadAll = () => {
      this.uploadAll();
    }

    this.dataAccess.getCollections().subscribe(res => {
      this.collections = res.data;
    });
  }

  public uploadAll() {
    var files = new Array<File>();
    this.uploader.queue.forEach(value => {
      console.log(value)
      files.push(value._file);
      this.dataAccess.uploadImages(value._file,this.chosenCollection.id).subscribe(event => {
        if (event.type === HttpEventType.UploadProgress) {

          // calculate the progress percentage
          value.progress = Math.round(100 * event.loaded / event.total);
          console.log(event.loaded);
          value.status=value.progress+"%";
          // pass the percentage into the progress-stream
        } else if (event instanceof HttpResponse) {

          // Close the progress-stream if we get an answer form the API
          // The upload is complete
          value.status="Complete";
          value.isSuccess=true;
        }
      });
    })

  }

  public fileOverBase (e : any): void {
    this.hasBaseDropZoneOver = e ;
  }

  public fileOverAnother (e : any): void {
    this.hasAnotherDropZoneOver = e ;
  }
}
