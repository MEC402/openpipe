
<table class="tg">
  <tr>
    <th class="tg-9wq8">Method</th>
    <th class="tg-c3ow">Path</th>
    <th class="tg-c3ow">Parameters</th>
    <th class="tg-c3ow">Parameter Description</th>
    <th class="tg-c3ow">Required</th>
  </tr>
  <tr>
    <td class="tg-c3ow" rowspan="3">GET</td>
    <td class="tg-c3ow" rowspan="3"><a href="http://mec402.boisestate.edu/cgi-bin/dataAccess/getCollections.py">http://mec402.boisestate.edu/cgi-bin/dataAccess/getCollections.py</a></td>
    <td class="tg-c3ow">collectionId</td>
    <td class="tg-c3ow">the specific id or all for all the collections</td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">start</td>
    <td class="tg-c3ow">starting id</td>
    <td class="tg-c3ow">no</td>
  </tr>
  <tr>
    <td class="tg-c3ow">end</td>
    <td class="tg-c3ow">ending id</td>
    <td class="tg-c3ow">no</td>
  </tr>
  <tr>
    <td class="tg-c3ow">GET</td>
    <td class="tg-c3ow"><a href="http://mec402.boisestate.edu/cgi-bin/dataAccess/createCollection.py">http://mec402.boisestate.edu/cgi-bin/dataAccess/createCollection.py</a></td>
    <td class="tg-c3ow">name</td>
    <td class="tg-c3ow">name of the new collection</td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow" rowspan="6">GET</td>
    <td class="tg-c3ow" rowspan="6"><a href="http://mec402.boisestate.edu/cgi-bin/dataAccess/addAsset.py">http://mec402.boisestate.edu/cgi-bin/dataAccess/addAsset.py</a></td>
    <td class="tg-c3ow">shortName</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">uri</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">idAtSource</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">sourceId</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">metaDataId</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">scope</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes<br></td>
  </tr>
  <tr>
    <td class="tg-c3ow" rowspan="3">GET</td>
    <td class="tg-c3ow" rowspan="3"><a href="http://mec402.boisestate.edu/cgi-bin/dataAccess/addAssetIntoCollection.py">http://mec402.boisestate.edu/cgi-bin/dataAccess/addAssetIntoCollection.py</a></td>
    <td class="tg-c3ow">assetId</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">collectionId</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">searchTerm</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">GET</td>
    <td class="tg-c3ow"><a href="http://mec402.boisestate.edu/cgi-bin/dataAccess/createMetaData.py">http://mec402.boisestate.edu/cgi-bin/dataAccess/createMetaData.py</a></td>
    <td class="tg-c3ow">-</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow"></td>
  </tr>
  <tr>
    <td class="tg-c3ow">POST</td>
    <td class="tg-c3ow"><a href="http://mec402.boisestate.edu/cgi-bin/dataAccess/createMetaTags.py">http://mec402.boisestate.edu/cgi-bin/dataAccess/createMetaTags.py</a></td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow"></td>
  </tr>
  <tr>
    <td class="tg-c3ow">GET</td>
    <td class="tg-c3ow"><a href="http://mec402.boisestate.edu/cgi-bin/dataAccess/getPublicAssetsInCollection.py">http://mec402.boisestate.edu/cgi-bin/dataAccess/getPublicAssetsInCollection.py</a></td>
    <td class="tg-c3ow">collectionId</td>
    <td class="tg-c3ow"></td>
    <td class="tg-c3ow">yes</td>
  </tr>
</table>
