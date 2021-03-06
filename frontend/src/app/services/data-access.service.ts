import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams, HttpRequest, HttpEventType, HttpResponse} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import set = Reflect.set;



@Injectable({
  providedIn: 'root',
})
export class DataAccessService {
  webServerURL;
  domainURL;
  constructor(private http: HttpClient) {
    this.webServerURL = 'http://mec402.boisestate.edu/cgi-bin/';
    this.domainURL = 'http://mec402.boisestate.edu/';
   // this.webServerURL = 'http://localhost/cgi-bin/';
  }

  public getMuseumData(searchTerm: string, museumName  , page: number , pageSize: number): Observable<Results> {
    const url = this.webServerURL + 'assetSources/rona/multiSources.py';
    const params = new HttpParams()
                  .set('q', searchTerm)
                  .set('name', museumName)
                  .set('p', String(page))
                  .set('ps', String(pageSize));
    return this.http.get<Results>(url, {params: params});
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


  public getFolders(): Observable<CollectionResults> {
    const url = this.domainURL + 'api/v1/folders';
    return this.http.get<CollectionResults>(url);
  }

  public getFolderDetails(folderId): Observable<FolderDetails> {
    const url = this.domainURL + 'api/v1/folder/' + folderId;
    return this.http.get<FolderDetails>(url);
  }

  public createCollection(name: string): Observable<InsertionResponse> {
    const url = this.webServerURL + 'dataAccess/createCollection.py';
    const params = new HttpParams().set('name', name);
    return this.http.get<InsertionResponse>(url, {params: params});
  }

  public uploadImages(file, folderId)  {
    const url = this.webServerURL + 'dataAccess/addUserAssets.py';

    // files.forEach(file => {
      if (folderId == -1)
        folderId = 130;
      const formData: FormData = new FormData();
      formData.append('file', file, file.name);
      formData.append('fileName', file.name);
      formData.append('folderId', folderId);
      const req = new HttpRequest('POST', url, formData, {
        reportProgress: true,
      });

      return this.http.request(req);
    // });
  }

  public saveAssetIntoCollection(asset, metaTags, collection, searchTerm, source, scope):
    Observable<InsertionResponse> {
    this.createMetaData().subscribe(res => {
      const metaDataId = res.result;
      this.saveAsset(asset, source, metaDataId, scope).subscribe(res0 => {
        const assetId = res0.result;
        this.addMetaTags(metaDataId, metaTags).subscribe(res1 => {
          this.addAssetToCollection(assetId, collection, searchTerm).subscribe(res2 => {
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
    const headers = new HttpHeaders({
      'Content-Type': 'text/plain',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post<InsertionResponse>(metaTagsURL, postBody);
  }

  public addAssetToCollection(assetId, collection, searchTerm): Observable<InsertionResponse> {
    const addAssetToCollectionURL = this.webServerURL + 'dataAccess/addAssetIntoCollection.py';
    const assetCollectionParams = new HttpParams().set('assetId', assetId)
      .set('collectionId', collection.id[0])
      .set('searchTerm', searchTerm);
    return this.http.get<InsertionResponse>(addAssetToCollectionURL, {params: assetCollectionParams});
  }

  public createMetaData(): Observable<InsertionResponse> {
    const assetMetaDataURL = this.webServerURL + 'dataAccess/createMetaData.py';
    return this.http.get<InsertionResponse>(assetMetaDataURL);
  }

  public getPublicAssetsInCollection(collectionId, p, ps): Observable<Assets> {
    const getAssetsInCollectionURL = this.webServerURL + 'dataAccess/getPublicAssetsInCollection.py';
    const assetsInCollectionParams = new HttpParams().set('collectionId', collectionId).set('p', p).set('ps', ps);
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
    });
  }

  public updateCanonicalMetaTag(id, newName) {
    const updateCanonicalMetaTagURL = this.webServerURL + 'dataAccess/updateCanonicalMetaTag.py';
    const updateCanonicalMetaTagParams = new HttpParams().set('id', id).set('name', newName);
    return this.http.get(updateCanonicalMetaTagURL, {params: updateCanonicalMetaTagParams}).subscribe(res => {
    });
  }

  public deleteCanonicalMetaTag(id) {
    const deleteCanonicalMetaTagURL = this.webServerURL + 'dataAccess/deleteCanonicalMetaTag.py';
    const deleteCanonicalMetaTagParams = new HttpParams().set('id', id);
    return this.http.get(deleteCanonicalMetaTagURL, {params: deleteCanonicalMetaTagParams}).subscribe(res => {
    });
  }

  public getAssetMetaTags(id): Observable<Results> {
    const getAssetMetaTagsURL = this.webServerURL + 'dataAccess/getAssetMetaTags.py';
    const getAssetMetaTagsParams = new HttpParams().set('assetId', id);
    return this.http.get<Results>(getAssetMetaTagsURL, {params: getAssetMetaTagsParams});
  }

  public getAllAssets(p, ps): Observable<Results> {
    // const getAllAssetURL = this.webServerURL + 'dataAccess/getAllAssets.py';
    const getAllAssetURL = 'http://mec402.boisestate.edu/wsgi/getAllAssets.wsgi';
    const getAssetParams = new HttpParams().set('p', p).set('ps', ps);
    return this.http.get<Results>(getAllAssetURL, {params: getAssetParams});
  }

  public getAssetsReport(id): Observable<Results> {
    const getAssetsReport = this.webServerURL + 'dataAccess/getAssetsReport.py';
    const getParams = new HttpParams().set('folderid', id);
    return this.http.get<Results>(getAssetsReport, {params: getParams});
  }

  public getAssetsMissingImageReport(): Observable<Results> {
    const getAssetsMissingImageReportURL = this.webServerURL + 'dataAccess/getAssetsWithoutImages.py';
    return this.http.get<Results>(getAssetsMissingImageReportURL);
  }

  // public getAssetsWithGUID(collectionId): Observable<Results> {
  //   const getAssetsMissingImageReportURL = this.webServerURL + 'dataAccess/getAssetsWithoutImages.py';
  //   return this.http.get<Results>(getAssetsMissingImageReportURL);
  // }
  //
  // getBooksAndMovies() {
  //   return Observable.forkJoin(
  //     this.http.get('/app/books.json').map((res:Response) => res.json()),
  //     this.http.get('/app/movies.json').map((res:Response) => res.json())
  //   );
  // }
  public deleteFolder(FolderId) {
    const deleteFolderURL = this.webServerURL + 'dataAccess/deleteFolder.py';
    const deleteFolderParams = new HttpParams().set('collectionId', FolderId);
    return this.http.get(deleteFolderURL, {params: deleteFolderParams}).subscribe(res => {
    });
  }

  public deleteFolderMember(folderId, assetId) {
    const deleteFolderMemberURL = this.webServerURL + 'dataAccess/deleteFolderMember.py';
    const deleteFolderMemberParams = new HttpParams().set('collectionId', folderId).set('assetId', assetId);
    return this.http.get(deleteFolderMemberURL, {params: deleteFolderMemberParams}).subscribe(res => {
    });
  }

  public updateMetaTag(metaDataId, oldTagName, oldValue, newTagName, newValue) {
    const updateMetaTagURL = this.webServerURL + 'dataAccess/updateMetaTag.py';
    const updateMetaTagParams = new HttpParams()
      .set('metaDataId', metaDataId)
      .set('oldTagName', oldTagName)
      .set('oldValue', oldValue)
      .set('newTagName', newTagName)
      .set('newValue', newValue);
    return this.http.get(updateMetaTagURL, {params: updateMetaTagParams});
  }

  public deleteMetaTag(metaDataId, tagName, value) {
    const deleteMetaTagURL = this.webServerURL + 'dataAccess/deleteMetaTag.py';
    const deleteMetaTagParams = new HttpParams()
      .set('metaDataId', metaDataId)
      .set('tagName', tagName)
      .set('value', value);
    return this.http.get(deleteMetaTagURL, {params: deleteMetaTagParams});
  }

  public insertMetaTag(metaDataId, tagName, value) {
    const insertMetaTagURL = this.webServerURL + 'dataAccess/addMetaTag.py';
    const insertMetaTagParams = new HttpParams()
      .set('metaDataId', metaDataId)
      .set('tagName', tagName)
      .set('value', value);
    return this.http.get(insertMetaTagURL, {params: insertMetaTagParams});
  }

  public updateFolder(folderId, newName, newImage, newVerified) {
    const updateFolderURL = this.webServerURL + 'dataAccess/updateFolder.py';
    const updateFolderParams = new HttpParams()
      .set('collectionId', folderId)
      .set('newName', newName)
      .set('newImage', newImage)
      .set('newVerified', newVerified ? '1' : '0');
    return this.http.get(updateFolderURL, {params: updateFolderParams});
  }

  updateTagMapping(mapId, tagMap) {
    const updateTM = this.webServerURL + 'dataAccess/updateTagMap.py';
    const params = new HttpParams()
      .set('id', mapId)
      .set('newTagMap', tagMap);
    return this.http.get(updateTM, {params: params});

  }

  public getAssetsWithGUID(): Observable<Results> {
    const assetsGUIDURL = this.webServerURL + '/openpipe/data/asset';
    return this.http.get<Results>(assetsGUIDURL);
  }

  public getGUID(GUIDURL): Observable<Results> {
    return this.http.get<Results>(GUIDURL);
  }

  public getWallAppSettings(): Observable<Results> {
    return this.http.get<Results>( this.webServerURL + 'dataAccess/settings/getWallAppSettings.py');
  }

  public setWallAppSettings(settings): Observable<InsertionResponse> {
    const metaTagsURL = this.webServerURL + 'dataAccess/settings/setWallAppSettings.py';
    const postBody = settings;
    const headers = new HttpHeaders({
      'Content-Type': 'text/json',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post<InsertionResponse>(metaTagsURL, postBody);
  }


  public getMuseumTagMapping(): Observable<Results> {
    return this.http.get<Results>( this.webServerURL + 'dataAccess/getMuseumTagMapping.py');
  }

  private messageSource = new BehaviorSubject([]);
  currentMessage = this.messageSource.asObservable();

  changeMessage(message) {
    this.messageSource.next(message);
  }


  private sampleTagSource = new BehaviorSubject([]);
  currentSampleTags = this.sampleTagSource.asObservable();
  changeSampleTags(message) {
    this.sampleTagSource.next(message);
  }

  getSampleMetaData(m: number) {
    if (m == 1) {
      return this.http.get<Results>( 'https://collectionapi.metmuseum.org/public/collection/v1/'
        + 'objects/' + '239154');
    } else if (m == 2) {
      const params = new HttpParams()
        .set('key', 'qvMYRE87')
        .set('format', 'json');
      return this.http.get<Results>( 'https://www.rijksmuseum.nl/api/en/collection/' + 'en-SK-A-4122'
        , {params: params});
    } else if (m == 3) {
      return this.http.get<Results>( 'https://openaccess-api.clevelandart.org/api/artworks/157235');
    }

  }

  public saveFolderLayout(layout): Observable<InsertionResponse> {
    const URL = this.webServerURL + 'dataAccess/saveFolderLayout.py';
    const postBody = layout;
    const headers = new HttpHeaders({
      'Content-Type': 'text/json',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post<InsertionResponse>(URL, postBody);
  }


}

class Results {
  total;
  data: any[];
  assets: any[];
}


class FolderDetails {
  folderInfo: any;
  metaTags: any;
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
