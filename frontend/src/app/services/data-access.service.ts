import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import * as url from 'url';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataAccessService {
  constructor(private http: HttpClient) { }

  public getMETsData(searchTerm: string , start: number , step: number) {
    // const url = 'http://mec402.boisestate.edu/cgi-bin/assetSources//mets.py';
    const url = 'http://mec402.boisestate.edu/cgi-bin/assetSources/mets.py';
    const params = new HttpParams().set('q', searchTerm).set('start', String(start)).set('step', String(step));
    return this.http.get(url, {params: params});
  }

  public getCollections(): Observable<CollectionResults> {
    const url = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/getCollections.py';
    const params = new HttpParams().set('collectionId', 'all');
    return this.http.get<CollectionResults>(url, {params: params});
  }

  public createCollection(name: string): Observable<InsertionResponse> {
    const url = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/createCollection.py';
    const params = new HttpParams().set('name', name);
    return this.http.get<InsertionResponse>(url, {params: params});
  }

  public saveAssetIntoCollection(asset, collection, searchTerm, source, scope): Observable<InsertionResponse> {
    this.createMetaData().subscribe(res => {
      const metaDataId = res.result;
      this.saveAsset(asset, source, metaDataId, scope).subscribe(res => {
        const assetId = res.result;
        this.addMetaTags(metaDataId, asset).subscribe(res => {
          this.addAssetToCollection(assetId, collection, searchTerm).subscribe(res => {
            console.log(res);
          });
        });
      });
    });
    return ;
  }

  public saveAsset(asset, source, metaDataId, scope): Observable<InsertionResponse> {
    const addAssetURL = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/addAsset.py';
    const assetParams = new HttpParams().set('shortName', asset.title)
      .set('uri', asset.uri)
      .set('idAtSource', asset.id)
      .set('sourceId', source.id)
      .set('metaDataId', metaDataId)
      .set('scope', scope);
    return this.http.get<InsertionResponse>(addAssetURL, {params: assetParams});
  }

  public addMetaTags(metaDataId, asset): Observable<InsertionResponse> {
    const metaTagsURL = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/createMetaTags.py';
    const postBody = {'metaDataId': metaDataId,
                      'title': asset.title,
                      'smallImage': asset.smallImage,
                      'largeImage': asset.largeImage};
    const headers = new HttpHeaders({
      'Content-Type': 'text/plain',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post<InsertionResponse>(metaTagsURL, postBody, {headers});
  }

  public addAssetToCollection(assetId, collection, searchTerm): Observable<InsertionResponse> {
    const addAssetToCollectionURL = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/addAssetIntoCollection.py';
    const assetCollectionParams = new HttpParams().set('assetId', assetId)
      .set('collectionId', collection.id)
      .set('searchTerm', searchTerm);
    return this.http.get<InsertionResponse>(addAssetToCollectionURL, {params: assetCollectionParams});
  }

  public createMetaData(): Observable<InsertionResponse> {
    const assetMetaDataURL = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/createMetaData.py';
    return this.http.get<InsertionResponse>(assetMetaDataURL);
  }

  public getPublicAssetsInCollection(collectionId): Observable<Assets> {
    const getAssetsInCollectionURL = 'http://mec402.boisestate.edu/cgi-bin/dataAccess/getPublicAssetsInCollection.py';
    const assetsInCollectionParams = new HttpParams().set('collectionId', collectionId);
    return this.http.get<Assets>(getAssetsInCollectionURL, {params: assetsInCollectionParams});
  }
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
