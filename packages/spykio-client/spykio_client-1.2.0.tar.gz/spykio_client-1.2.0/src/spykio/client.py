import requests

class SpykioClient:
    def __init__(self, api_key=None, base_url="https://api.spyk.io"):
        self.api_key = api_key
        self.base_url = base_url
        self.query = self._create_query()
        self.files = self._create_files()
        self.documents = self._create_documents()
    
    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'spykio-client-python',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def _create_query(self):
        class Query:
            def __init__(self, client):
                self.client = client
            
            def search(self, index, user_query, accurate_match=False, get_relevant_info=False):
                """Search for information in a specific index."""
                options = {
                    'index': index,
                    'userQuery': user_query,
                    'accurateMatch': accurate_match,
                    'getRelevantInfo': get_relevant_info
                }
                
                response = requests.post(
                    f"{self.client.base_url}/query",
                    headers=self.client._get_headers(),
                    json=options
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Filter unwanted fields
                if 'metrics' in response_data and 'tokenUsage' in response_data['metrics']:
                    del response_data['metrics']['tokenUsage']
                
                if 'documents' in response_data and isinstance(response_data['documents'], list):
                    filtered_docs = []
                    for doc in response_data['documents']:
                        filtered_docs.append({
                            'id': doc.get('id'),
                            'content': doc.get('content'),
                            'summary': doc.get('summary'),
                            'created_at': doc.get('created_at')
                        })
                    response_data['documents'] = filtered_docs
                
                return response_data
        
        return Query(self)
    
    def _create_files(self):
        class Files:
            def __init__(self, client):
                self.client = client
            
            def upload(self, index, mime_type=None, base64_string=None, content=None):
                """Upload a file or content to a specific index."""
                request_body = {'index': index}
                
                if content is not None:
                    request_body['content'] = content
                else:
                    request_body['mimeType'] = mime_type
                    request_body['base64String'] = base64_string
                
                response = requests.post(
                    f"{self.client.base_url}/uploadFile",
                    headers=self.client._get_headers(),
                    json=request_body
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Filter out unwanted fields
                if 'categorization' in response_data:
                    del response_data['categorization']
                
                if 'metrics' in response_data:
                    del response_data['metrics']
                
                return response_data
                
            def remove(self, index, document_id, region="EU"):
                """Remove a document from an index.
                
                Args:
                    index (str): The name of the index containing the document
                    document_id (str): The ID of the document to remove
                    region (str, optional): The region where the index is located. Defaults to "EU"
                    
                Returns:
                    dict: Response data from the API
                """
                if not index:
                    raise ValueError("Missing required parameter: index")
                
                if not document_id:
                    raise ValueError("Missing required parameter: document_id")
                
                request_body = {
                    'index': index,
                    'documentId': document_id,
                    'region': region
                }
                
                response = requests.delete(
                    f"{self.client.base_url}/documents/remove",
                    headers=self.client._get_headers(),
                    json=request_body
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Filter out sensitive metrics data
                if 'metrics' in response_data:
                    del response_data['metrics']
                
                return response_data
        
        return Files(self)

    def _create_documents(self):
        class Documents:
            def __init__(self, client):
                self.client = client
            
            def list(self, index, region="EU", limit=100, offset=0):
                """Retrieve a paginated list of all documents in an index.
                
                Args:
                    index (str): The name of the index to list documents from
                    region (str, optional): The region where the index is located. Defaults to "EU"
                    limit (int, optional): Maximum number of documents to return. Defaults to 100
                    offset (int, optional): Number of documents to skip for pagination. Defaults to 0
                    
                Returns:
                    dict: Response data from the API containing documents and pagination info
                """
                if not index:
                    raise ValueError("Missing required parameter: index")
                
                # Validate numeric parameters
                if not isinstance(limit, int) or limit <= 0:
                    raise ValueError("Invalid limit parameter. Must be a positive number.")
                
                if not isinstance(offset, int) or offset < 0:
                    raise ValueError("Invalid offset parameter. Must be a non-negative number.")
                
                params = {
                    'index': index,
                    'region': region,
                    'limit': limit,
                    'offset': offset
                }
                
                response = requests.get(
                    f"{self.client.base_url}/documents/list",
                    headers=self.client._get_headers(),
                    params=params
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Filter out sensitive metrics data
                if 'metrics' in response_data:
                    del response_data['metrics']
                
                return response_data
            
            def extract(self, index, document_id, user_query, region="EU"):
                """Extract specific information from a document based on a query.
                
                Args:
                    index (str): The name of the index containing the document
                    document_id (str): The ID of the document to extract information from
                    user_query (str): The query to extract specific information from the document
                    region (str, optional): The region where the index is located. Defaults to "EU"
                    
                Returns:
                    dict: Response data from the API containing relevant sections and document summary
                """
                if not index:
                    raise ValueError("Missing required parameter: index")
                
                if not document_id:
                    raise ValueError("Missing required parameter: document_id")
                
                if not user_query:
                    raise ValueError("Missing required parameter: user_query")
                
                request_body = {
                    'index': index,
                    'documentID': document_id,
                    'userQuery': user_query,
                    'region': region
                }
                
                response = requests.post(
                    f"{self.client.base_url}/extractFromDocument",
                    headers=self.client._get_headers(),
                    json=request_body
                )
                
                response.raise_for_status()
                response_data = response.json()
                
                # Filter out sensitive metrics data if present
                if 'metrics' in response_data and 'tokenUsage' in response_data['metrics']:
                    del response_data['metrics']['tokenUsage']
                
                return response_data
        
        return Documents(self)
