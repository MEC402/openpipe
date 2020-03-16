import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams, HttpRequest, HttpEventType, HttpResponse} from '@angular/common/http';
import * as url from 'url';
import {Observable} from 'rxjs';
import {FileItem} from 'ng2-file-upload';
import {log} from "util";

@Injectable({
  providedIn: 'root',
})
export class DataAccessService {
  webServerURL;
  constructor(private http: HttpClient) {
    this.webServerURL = 'http://mec402.boisestate.edu/cgi-bin/';
   // this.webServerURL = 'http://localhost/cgi-bin/';
  }

  public getMuseumData(searchTerm: string, museumName  , page: number , pageSize: number) {
    const url = this.webServerURL + 'assetSources/museums.py';
    const params = new HttpParams()
                  .set('q', searchTerm)
                  .set('name', museumName)
                  .set('p', String(page))
                  .set('ps', String(pageSize));
    return this.http.get(url, {params: params});
  }

  public getMETsData(searchTerm: string , start: number , step: number) {
    const url = this.webServerURL + 'assetSources/mets.py';
    const params = new HttpParams().set('q', searchTerm).set('start', String(start)).set('step', String(step));
    return this.http.get(url, {params: params});
  }

  public getRijksData(searchTerm: string , start: number , step: number) {
    const url = this.webServerURL + 'assetSources/rijks.py';
    const params = new HttpParams().set('q', searchTerm).set('start', String(start)).set('step', String(step));
    return this.http.get(url, {params: params});
  }

  public getClevelandData(searchTerm: string , start: number , step: number) {
    const url = this.webServerURL + 'assetSources/cleveland.py';
    const params = new HttpParams().set('q', searchTerm).set('start', String(start)).set('step', String(step));
    return this.http.get(url, {params: params});
  }

  public getCollections(): Observable<CollectionResults> {
    const url = this.webServerURL + 'dataAccess/getCollections.py';
    const params = new HttpParams().set('collectionId', 'all');
    return this.http.get<CollectionResults>(url, {params: params});
  }

  public createCollection(name: string): Observable<InsertionResponse> {
    const url = this.webServerURL + 'dataAccess/createCollection.py';
    const params = new HttpParams().set('name', name);
    return this.http.get<InsertionResponse>(url, {params: params});
  }

  public uploadImages(files : File[])  {
    const url = this.webServerURL + 'dataAccess/addUserAssets.py';
    const postBody = { "files": files };

    files.forEach(file => {

      const formData: FormData = new FormData();
      formData.append('file', file, file.name);
      const req = new HttpRequest('POST', url, formData, {
        reportProgress: true
      })


      this.http.request(req).subscribe(event => {
        if (event.type === HttpEventType.UploadProgress) {

          // calculate the progress percentage
          const percentDone = Math.round(100 * event.loaded / event.total);
          console.log(percentDone);
          // pass the percentage into the progress-stream
        } else if (event instanceof HttpResponse) {

          // Close the progress-stream if we get an answer form the API
          // The upload is complete
          console.log("done");
        }
      });



    });


    /*

    console.log(files[0]);
    console.log(formData);
   const headers = new HttpHeaders({
      'Content-Type': 'image/jpeg',
      'Access-Control-Allow-Origin': '',
   });
    console.log(files);
    this.http.post<any>(url, formData, { headers }).subscribe(data => {
      console.log(data);
    });
    */

  }

  public saveAssetIntoCollection(asset, metaTags, collection, searchTerm, source, scope): Observable<InsertionResponse> {
    this.createMetaData().subscribe(res => {
      const metaDataId = res.result;
      this.saveAsset(asset, source, metaDataId, scope).subscribe(res => {
        const assetId = res.result;
        this.addMetaTags(metaDataId, metaTags).subscribe(res => {
          console.log("after adding metaTags");
          console.log(res);
          this.addAssetToCollection(assetId, collection, searchTerm).subscribe(res => {
            console.log("test");
            console.log(res);
          });
        });
      });
    });
    return ;
  }

  public saveAsset(asset, source, metaDataId, scope): Observable<InsertionResponse> {
    const addAssetURL = this.webServerURL + 'dataAccess/addAsset.py';
    const assetParams = new HttpParams().set('shortName', asset.title)
      .set('uri', asset.uri)
      .set('idAtSource', asset.id)
      .set('sourceId', source.id)
      .set('metaDataId', metaDataId)
      .set('scope', scope);
    return this.http.get<InsertionResponse>(addAssetURL, {params: assetParams});
  }

  public addMetaTags(metaDataId, metaTags): Observable<InsertionResponse> {
    const metaTagsURL = this.webServerURL + 'dataAccess/createMetaTags.py';
    metaTags['metaDataId'] = metaDataId;
    const postBody = metaTags;
    console.log(postBody);
    const headers = new HttpHeaders({
      'Content-Type': 'text/plain',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post<InsertionResponse>(metaTagsURL, postBody);
  }

  public addAssetToCollection(assetId, collection, searchTerm): Observable<InsertionResponse> {
    const addAssetToCollectionURL = this.webServerURL + 'dataAccess/addAssetIntoCollection.py';
    console.log(collection.id)
    console.log(collection.id[0])
    const assetCollectionParams = new HttpParams().set('assetId', assetId)
      .set('collectionId', collection.id[0])
      .set('searchTerm', searchTerm);
    return this.http.get<InsertionResponse>(addAssetToCollectionURL, {params: assetCollectionParams});
  }

  public createMetaData(): Observable<InsertionResponse> {
    const assetMetaDataURL = this.webServerURL + 'dataAccess/createMetaData.py';
    return this.http.get<InsertionResponse>(assetMetaDataURL);
  }

  public getPublicAssetsInCollection(collectionId): Observable<Assets> {
    const getAssetsInCollectionURL = this.webServerURL + 'dataAccess/getPublicAssetsInCollection.py';
    const assetsInCollectionParams = new HttpParams().set('collectionId', collectionId);
    return this.http.get<Assets>(getAssetsInCollectionURL, {params: assetsInCollectionParams});
  }

  public getCanonicalMetaTags(): Observable<Collection[]> {
    const getCanonicalMetaTagsURL = this.webServerURL + 'dataAccess/getCanonicalMetaTags.py';
    return this.http.get<Collection[]>(getCanonicalMetaTagsURL);
  }

  public addCanonicalMetaTag(name) {
    const addCanonicalMetaTagURL = this.webServerURL + 'dataAccess/addCanonicalMetaTag.py';
    const addCanonicalMetaTagParams = new HttpParams().set('name', name);
    this.http.get(addCanonicalMetaTagURL, {params: addCanonicalMetaTagParams}).subscribe(res => {
      console.log(res);
    });
  }

  public updateCanonicalMetaTag(id, newName) {
    const updateCanonicalMetaTagURL = this.webServerURL + 'dataAccess/updateCanonicalMetaTag.py';
    const updateCanonicalMetaTagParams = new HttpParams().set('id', id).set('name', newName);
    return this.http.get(updateCanonicalMetaTagURL, {params: updateCanonicalMetaTagParams}).subscribe(res => {
      console.log(res);
    });
  }

  public deleteCanonicalMetaTag(id) {
    const deleteCanonicalMetaTagURL = this.webServerURL + 'dataAccess/deleteCanonicalMetaTag.py';
    const deleteCanonicalMetaTagParams = new HttpParams().set('id', id);
    return this.http.get(deleteCanonicalMetaTagURL, {params: deleteCanonicalMetaTagParams}).subscribe(res => {
      console.log(res);
    });
  }

  public getAssetMetaTags(id): Observable<Results> {
    const getAssetMetaTagsURL = this.webServerURL + 'dataAccess/getAssetMetaTags.py';
    const getAssetMetaTagsParams = new HttpParams().set('assetId', id);
    return this.http.get<Results>(getAssetMetaTagsURL, {params: getAssetMetaTagsParams});
  }

  public getAllAssets(): Observable<Results> {
    const getAllAssetURL = this.webServerURL + 'dataAccess/getAllAssets.py';
    return this.http.get<Results>(getAllAssetURL);
  }

  public getAssetsReport(): Observable<Results> {
    const getAssetsReport = this.webServerURL + 'dataAccess/getAssetsReport.py';
    return this.http.get<Results>(getAssetsReport);
  }

  public getAssetsMissingImageReport(): Observable<Results> {
    const getAssetsMissingImageReportURL = this.webServerURL + 'dataAccess/getAssetsWithoutImages.py';
    return this.http.get<Results>(getAssetsMissingImageReportURL);
  }

}


class Results {
  total;
  data: any[];
}

class CollectionResults {
  total;
  data: Collection[];
}
class Collection {
  id;
  name;
  timestamp;
}

class InsertionResponse {
  result;
}

class Assets {
  total;
  data: AssetMainMetaData[];
}

class AssetMainMetaData {
  id;
  title;
  smallImage;
  largeImage;
}
