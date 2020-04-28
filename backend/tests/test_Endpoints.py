import requests


class TestEndpoints():
    """
        Class for testing the end points.
        url points to the API base.
    """
    url='http://mec402.boisestate.edu/cgi-bin/'
    def test_allSources(self):
        """
            test if the allSourses endpoint is working
        """
        # service name that is required. This will be appended to the base url.
        serviceName = "assetSources/allSources.py"
        # Request parameters, each parameter should be a key value pair in the dictionary
        params = {'q': 'cats'}
        # Sending the get request and get the response
        response = requests.get(url=self.url + serviceName, params=params)
        data = response.json()
        # you can make any assertion you want this just an example
        assert ("total" in data)