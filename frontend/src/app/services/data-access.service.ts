import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import * as url from 'url';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataAccessService {
  webServerURL;
  constructor(private http: HttpClient) {
    this.webServerURL = 'http://mec402.boisestate.edu/cgi-bin/';
    //this.webServerURL = 'http://localhost/cgi-bin/';
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

  public saveAssetIntoCollection(asset, metaTags, collection, searchTerm, source, scope): Observable<InsertionResponse> {
    this.createMetaData().subscribe(res => {
      const metaDataId = res.result;
      this.saveAsset(asset, source, metaDataId, scope).subscribe(res => {
        const assetId = res.result;
        this.addMetaTags(metaDataId, metaTags).subscribe(res => {
          this.addAssetToCollection(assetId, collection, searchTerm).subscribe(res => {
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
    return this.http.post<InsertionResponse>(metaTagsURL, postBody, {headers});
  }

  public addAssetToCollection(assetId, collection, searchTerm): Observable<InsertionResponse> {
    const addAssetToCollectionURL = this.webServerURL + 'dataAccess/addAssetIntoCollection.py';
    const assetCollectionParams = new HttpParams().set('assetId', assetId)
      .set('collectionId', collection.id)
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

  public getAllAssets() {
    const getAllAssetURL = this.webServerURL + 'dataAccess/getAllAssets.py';
    return this.http.get(getAllAssetURL);
  }

  public getAssetsMissingImageReport() {
    const getAssetsMissingImageReportURL = this.webServerURL + 'dataAccess/getAssetsReport.py';
    return this.http.get(getAssetsMissingImageReportURL);
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
