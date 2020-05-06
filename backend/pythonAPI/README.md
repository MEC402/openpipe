# VizLab API 
VizLab API is designed to explore museums’ collections. The API provides direct access to the data of the museums.


 1. Must register with yahoo email
    
    
 2. Go to    [https://www.flickr.com/services/apps/create/apply/](https://www.flickr.com/services/apps/create/apply/)
    
    
 3. Click Apply for a non-commercial key
    
    
 4. Put “CatApp” as name of app.  
    Write something on what you try to building.   
    Click both check box.    
    Obtain the following keys access key my secret key
    
    **Key:**  
    **68cc14482d6be482f88a9f5c41e9a___**
    
    **Secret:**  
    **5831bf74fb370___**
    
    
 5. Go    [https://www.flickr.com/services/api/](https://www.flickr.com/services/api/)
    
    Here, many API methods are available that you might want to use and
    each of these methods comes with their own parameters
    
    
 6. **Click [flickr.photos.search](https://www.flickr.com/services/api/flickr.photos.search.html)
    under photos section. We will see many options here. Go to bottom of
    the page and click** [API Explorer :
    flickr.photos.search](https://www.flickr.com/services/api/explore/flickr.photos.search)
    
    **It will direct to** [https://www.flickr.com/services/api/explore/flickr.photos.search](https://www.flickr.com/services/api/explore/flickr.photos.search)
    
   
 7.  **Check the tags option and put “cats” as value.**
    
    scroll down and choose JSON as output and click on Sign call with no
    user token? And click call method.
    
    You will get a response. Click the URL at bottom and get some JSON
    code.
    
    
 8. **Create a file and name index.php and paste the following**
    
  <?php
        $tag='cat'
         $url = 'https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=1b9b13d16773af7a80a1abd0e94e56ba&tags='.$tag.'&format=json&nojsoncallback=1’;

$data=file_get_contents($url);
print_r($data);
        