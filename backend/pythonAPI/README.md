

# VizLab API 
VizLab API is designed to explore museums’ collections. The API provides direct access to the data of the museums.
```python
import urllib3  # first, import the urllib3 module:
http = urllib3.PoolManager()   # a PoolManager instance to make requests. This object handles all of the details of connection pooling

# Find all of the objects with the word "cat" in the title and return only a few fields per record
def url():
    s = input("please enter a museum name: ")
    new_string = s 
    return new_string
def object_name():
    s1 = input("please enter a object name: ")
    object_string = s1
    return object_string

print(object_name());

r = http.request('GET', url(),
			# request() to make requests using any HTTP verb
    fields = {
	'apikey': 'YOUR APIKEY HERE',
        'title': object_string(),
        'fields': 'objectnumber,title,dated'
    })

print(r.status, r.data)

```

## urllib3
urllib3 is a powerful, _sanity-friendly_ HTTP client for Python. urllib3 brings many critical features that are missing from the Python standard libraries: Connection pooling, Client-side SSL/TLS verification, etc.


## **Installing**

urllib3 can be installed with [pip](https://pip.pypa.io/):

    $ pip install urllib3
Alternatively, you can grab the latest source code from [GitHub](https://github.com/urllib3/urllib3):

    $ git clone git://github.com/urllib3/urllib3.git
    $ python setup.py install
	
	
## Flickr API Keys
We need to create a pair of Flickr API keys by visiting https://www.flickr.com/services/api/keys/. Note: A Yahoo! account is required to generate the API keys.Flickr will generate two keys:
`•	A public key, which they call key
•	A private key, which they call secret`
##### flickrapi installation
Create a virtual environment, and then install the flickrapi Python library via
    `$ pip install flickrapi`
Search Flickr Images
Here's an example that searches Flickr for the term "kitten" and retrieves the first 10 results.
```python
from flickrapi import FlickrAPI

FLICKR_PUBLIC = 'Your Flickr Key'
FLICKR_SECRET = 'Your Flickr Secret Key'

flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
cats = flickr.photos.search(text='kitten', per_page=5, extras=extras)
photos = cats['photos']
from pprint import pprint
pprint(photos)

```

