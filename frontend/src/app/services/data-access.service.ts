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
  awsApiDomainName;
  constructor(private http: HttpClient) {
    this.webServerURL = 'http://mec402.boisestate.edu/cgi-bin/';
    this.domainURL = 'http://mec402.boisestate.edu/';
   // this.webServerURL = 'http://localhost/cgi-bin/';
    this.awsApiDomainName = 'https://lmod9t47la.execute-api.us-west-2.amazonaws.com/v1/';
  }

  public getMuseumInfo():  Observable<MuseumInfo> {
    const url = this.webServerURL + 'assetSources/rona/museumsInfo.py';
    return this.http.get<MuseumInfo>(url);
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

  public getFolders(p, ps): Observable<CollectionResults> {
    const url = this.awsApiDomainName + 'folders';
    const params = new HttpParams()
      .set('p', p)
      .set('ps', ps);
    return this.http.get<CollectionResults>(url, {params: params});
  }

  public getFolderDetails(folderId): Observable<FolderDetails> {
    const url = this.awsApiDomainName + 'folder';
    const params = new HttpParams()
      .set('id', folderId);
    return this.http.get<FolderDetails>(url, {params: params});
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
    const metaTagsURL = this.awsApiDomainName + 'metatags';
    metaTags['metaDataId'] = metaDataId;
    const postBody = metaTags;
    const headers = new HttpHeaders({
      'Content-Type': 'text/plain',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.put<InsertionResponse>(metaTagsURL, postBody);
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

  public getFolderAssets(collectionId, p, ps): Observable<Assets> {
    const getAssetsInCollectionURL = this.awsApiDomainName + 'folderassets';
    const assetsInCollectionParams = new HttpParams().set('folderId', collectionId).set('p', p).set('ps', ps);
    return this.http.get<Assets>(getAssetsInCollectionURL, {params: assetsInCollectionParams});
  }

  public getChangedAssets(date, p, ps): Observable<Assets> {
    const getAssetsInCollectionURL = this.awsApiDomainName + 'search/changed-assets';
    const assetsInCollectionParams = new HttpParams().set('date', date).set('p', p).set('ps', ps);
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
    const updateFolderURL = this.awsApiDomainName + 'folder';
    const updateFolderParams = new HttpParams()
      .set('folderId', folderId)
      .set('newName', newName)
      .set('newImage', newImage)
      .set('newVerified', newVerified ? '1' : '0');
    return this.http.put(updateFolderURL, {params: updateFolderParams});
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

  public loadFolderLayout(folderId): Observable<Results> {
    const url = this.awsApiDomainName + 'folder/layout';
    const params = new HttpParams()
      .set('folderId', folderId);
    return this.http.get<Results>(url, {params: params});
  }

  public saveAssetChanges(mid, data) {
    const URL = this.awsApiDomainName + 'metatags';
    const postBody = {'metaDataId': mid, 'data': data};
    const headers = new HttpHeaders({
      'Content-Type': 'text/json',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post<InsertionResponse>(URL, postBody);
  }


  public saveMetaTagChanges(mid, data) {
    const URL = this.awsApiDomainName + 'multitag';
    let d={"metaDataId":mid,"insert":{},"update":{}}
    console.log(data)
    for (const [key, value] of Object.entries(data)) {
      console.log(key)
      if (key.includes("New_tag")) {
        let tagName = key.split(':')[1];
        if (tagName in d.insert){
          d.insert[tagName].push(value);
        }
        else{
          d.insert[tagName]=[value];
        }
      }
      else {
        d.update[key]=value;
      }
      console.log(d)
    }

    const postBody = d;
    const headers = new HttpHeaders({
      'Content-Type': 'text/json',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post<InsertionResponse>(URL, postBody);
  }


  public getAssetByMetaDataId(mid): Observable<Asset> {
    const url = this.awsApiDomainName + 'asset';
    const params = new HttpParams()
      .set('mid', mid);
    return this.http.get<Asset>(url, {params: params});
  }

  public getTopicByCode(code, page, pageSize): Observable<Results> {
    const url = this.awsApiDomainName + 'topic';
    const params = new HttpParams()
      .set('code', code)
      .set('p', page)
      .set('ps', pageSize);
    return this.http.get<Results>(url, {params: params});
  }

  public getTopicAliases(topicId, page, pageSize): Observable<Results> {
    const url = this.awsApiDomainName + 'topicaliases';
    const params = new HttpParams()
      .set('topicId', topicId)
      .set('p', page)
      .set('ps', pageSize);
    return this.http.get<Results>(url, {params: params});
  }

  public updateTopic(topicId, updateData) {
    const updateTopicURL = this.awsApiDomainName + 'topic';
    let updateTopicParams = new HttpParams();
    updateTopicParams = updateTopicParams.set('id', topicId);
    for (const [key, value] of Object.entries(updateData)) {
      updateTopicParams = updateTopicParams.set(key, String(value));
    }
    return this.http.put(updateTopicURL, {params: updateTopicParams});
  }


  public searchTopic(term, code, page, pageSize) {
    const searchTopicURL = this.awsApiDomainName + 'search/topic';
    const params = new HttpParams()
      .set('term', term)
      .set('code', code)
      .set('p', page)
      .set('ps', pageSize);
    return this.http.get<Results>(searchTopicURL, {params: params});
  }

  public mergeTopics(mergeData) {
    const URL = this.awsApiDomainName + 'topic/merge';
    return this.http.post<InsertionResponse>(URL, mergeData);
  }

  public deleteAssetFromFolder(assetId, folderId) {
    const URL = this.awsApiDomainName + 'folderassets';
    const params = new HttpParams()
      .set('assetId', assetId)
      .set('folderId', folderId);
    let options = { params: params };

    return this.http.delete<InsertionResponse>(URL, options);
  }

  public getUserInfo(token) {
    const url = 'https://www.googleapis.com/oauth2/v3/userinfo';
    const params = new HttpParams().set('access_token', token);
    return this.http.get<UserInfo>(url, {params: params});
  }

  public addAssetsToFolder(data) {
    const URL = this.awsApiDomainName + 'folderassets';
    const postBody = {'data': data};
    const headers = new HttpHeaders({
      'Content-Type': 'text/json',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post(URL, postBody);
  }
}


class UserInfo {
  sub;
  name;
  given_name;
  family_name;
  picture;
  locale;
}

class Results {
  total;
  data: any[];
  assets: any[];
}

class MuseumInfo {
  museum1: any[];
}

class Asset {
  total;
  tagData;
}

class FolderDetails {
  insertTime;
  image;
  id;
  name;
  metaDataId;
  lastModified;
  verified;
  note;
  layoutType;
}

class CollectionResults {
  total;
  data: Collection[];
}
class Collection {
  note;
  metaDataId;
  id;
  insertTime;
  verified;
  lastModified;
  name;
  layoutType;
  image;
  assetCount;
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
