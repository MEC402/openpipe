import {Component , OnInit } from '@angular/core';
import {FileUploader , FileItem } from 'ng2-file-upload';
import {DataAccessService } from '../../services/data-access.service';

//tslint:disable

// const URL = '/api/';
const URL = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/addUserAssets.py';

@ Component ({
  selector : 'ngx-uploader',
  templateUrl : './uploader.component.html',
  styleUrls : ['./uploader.component.scss']
})
export class UploaderComponent  {
  public uploader : FileUploader = new FileUploader ({url : URL });
  public hasBaseDropZoneOver : boolean = false;
  public hasAnotherDropZoneOver : boolean = false;

  constructor(private dataAccess : DataAccessService ) {
  }

  ngOnInit() {
    //this.uploader.uploadAll = () => this.uploadAll();
  }

  public uploadAll() {
    console.log(this.uploader.queue);
    
    //this.dataAccess.uploadImages(null);
  }

  public fileOverBase (e : any): void {
    this.hasBaseDropZoneOver = e ;
  }

  public fileOverAnother (e : any): void {
    this.hasAnotherDropZoneOver = e ;
  }
}
