import tempfile
import os
import re
import requests
import aiohttp
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Any

from global_parser.exceptions import DownloadError, InvalidFileType, ProcessingError
from global_parser.file_parser.type.file import parse_pdf, parse_docx, parse_pdf_with_images, parse_docx_with_images, parse_csv, parse_csv_without_template, parse_xlsx, parse_xlsx_without_template, download_and_extract_headers_xlsx, parse_pptx, parse_txt, parse_pdf_with_links, parse_pdf_with_links_and_images
from global_parser.file_parser.type.audio import parse_audio
from global_parser.file_parser.type.image import process_image_with_pixtral
from global_parser.url_parser.parser import extract_text_from_url

class FileParser:
    def __init__(self, max_workers: int = None):
        """
        Initialize FileParser with optional max workers for thread pool
        
        Args:
            max_workers: Maximum number of threads for parallel processing
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def download_file(self, s3_url: str) -> str:
        """
        Downloads a file from an S3 URL and saves it temporarily.
        
        Args:
            s3_url: S3 URL of the file
            
        Returns:
            str: Local path of the downloaded file
            
        Raises:
            DownloadError: If file download fails
        """
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file_path = temp_file.name
            temp_file.close()
            
            connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification
            
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(s3_url) as response:
                    if response.status != 200:
                        raise DownloadError(f"Failed to download file from S3: Status {response.status}")
                    with open(temp_file_path, 'wb') as f:
                        f.write(await response.read())
            
            return temp_file_path
        except Exception as e:
            raise DownloadError(f"Error downloading file: {str(e)}")

    async def valid_url(self, url):
        try:
            # Ensure the URL has a valid scheme and netloc
            parsed = urlparse(url)
            if not (parsed.scheme and parsed.netloc):
                return False

            # Make a HEAD request to check the URL's validity
            response = requests.head(url, allow_redirects=True, timeout=5)
            # A valid URL should return a status code in the 200-399 range
            #print(response.status_code)
            return 200 <= response.status_code < 400
        except requests.RequestException:
            # If an exception occurs, the URL is invalid or unreachable
            return False

    async def remove_broken_links(self, content):
    # Define a regex pattern to extract URLs
        url_pattern = r"https?://[^\s]+"
        urls = re.findall(url_pattern, content)

        # Remove broken URLs from the content
        for url in urls:
            if not await self.valid_url(url):
                content = content.replace(url, "")
        return content
    
    async def process_file(self, file_url: str, input: Optional[str] = None, sent_from: Optional[str] = None) -> Any:
        """
        Processes a file based on its type and extracts text or data.
        
        Args:
            file_url: URL of the file to process
            input: Optional input template or configuration
            sent_from: Optional source identifier
            
        Returns:
            Any: Processed file content
            
        Raises:
            ProcessingError: If file processing fails
            InvalidFileType: If file type is not supported
        """
        temp_file_path = None
        try:
            temp_file_path = await self.download_file(file_url)
            file_path = urlparse(file_url).path.lower()
            if file_path.endswith('.pdf'):
                text= parse_pdf_with_links_and_images(temp_file_path) if sent_from == 'vaia_client' else parse_pdf(temp_file_path)
            elif file_path.endswith('.doc'):
                text=  parse_docx(temp_file_path)
            elif file_path.endswith('.docx'):
                text=  parse_docx_with_images(temp_file_path)
            elif file_path.endswith('.csv'):
                text=  parse_csv_without_template(temp_file_path) if sent_from == 'vaia_client' else parse_csv(temp_file_path, input)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                if sent_from == 'vaia_client':
                    headers = download_and_extract_headers_xlsx(temp_file_path)
                    text=  headers + "\n"+ parse_xlsx(temp_file_path, headers) + "\n" + parse_xlsx_without_template(temp_file_path)
                else:
                    text=  parse_xlsx(temp_file_path, input)
            elif file_path.endswith('.pptx'):
                text=  parse_pptx(temp_file_path)
            elif file_path.endswith('.txt'):
                text=  parse_txt(temp_file_path)
            elif file_path.endswith('.mp3'):
                text=  await parse_audio(temp_file_path)  # Audio parsing might be async
            elif file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                text=  process_image_with_pixtral(file_url)
            else:
                return 'Failed to extract data, file type not found.'

            print(text)
            # ✅ Remove broken links from extracted text
            cleaned_text = await self.remove_broken_links(text)

            return cleaned_text
        
        except Exception as e:
            if isinstance(e, InvalidFileType):
                raise
            raise ProcessingError(f"Error processing file: {str(e)}")
        
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception as cleanup_error:
                    print(f"Error cleaning up temporary file {temp_file_path}: {cleanup_error}") 

class UrlParser:
    def __init__(self, max_workers: int = None):
        """
        Initialize UrlParser with optional max workers for thread pool
        
        Args:
            max_workers: Maximum number of threads for parallel processing
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def parse_url(self,url,frequency:Optional[str]=None,sent_from:Optional[str]=None):
        text = await extract_text_from_url(url, frequency,sent_from)  
        return text
