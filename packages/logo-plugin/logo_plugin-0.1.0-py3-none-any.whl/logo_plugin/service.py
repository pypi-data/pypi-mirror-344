import argparse
import os
import requests
import gridfs
from pymongo import MongoClient
from .config import MONGO_URI, DB_NAME, API_BASE_URL, API_PATH_TOKEN, API_KEY

class LogoService:
    """
    Service to fetch, store, and retrieve company logos by root domain.
    """
    def __init__(self, mongo_uri=MONGO_URI, db_name=DB_NAME):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)

    def fetch_and_store(self, root_domain: str) -> str:
        """
        Fetches a logo via API and stores it in GridFS. Returns the stored file_id.
        """
        url = f"{API_BASE_URL}/{root_domain}?token={API_PATH_TOKEN}&retina=true"
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch logo: {response.status_code}")
        image_data = response.content

        # Remove any existing logo for this domain
        existing = self.fs.find_one({'metadata.root_domain': root_domain})
        if existing:
            self.fs.delete(existing._id)

        metadata = {
            'filename': f'{root_domain}_logo.png',
            'root_domain': root_domain
        }
        file_id = self.fs.put(image_data, metadata=metadata)
        return str(file_id)

    def retrieve(self, root_domain: str, output_dir: str = '.') -> str:
        """
        Retrieves the stored logo by root domain, writes to output_dir, and returns the filepath.
        Returns None if not found.
        """
        file = self.fs.find_one({'metadata.root_domain': root_domain})
        if not file:
            return None
        filename = file.metadata.get('filename', f'{root_domain}_logo.png')
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'wb') as f:
            f.write(file.read())
        return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Fetch, store, and retrieve a company logo by root domain'
    )
    parser.add_argument('root_domain', help='Root domain (e.g. example.com)')
    parser.add_argument(
        '--output-dir', default='.',
        help='Local directory to save the retrieved logo (default: current dir)'
    )
    args = parser.parse_args()

    service = LogoService()
    try:
        file_id = service.fetch_and_store(args.root_domain)
        print(f"Stored logo with file_id: {file_id}")
    except Exception as e:
        print(f"Error during fetch/store: {e}")
        return

    output_path = service.retrieve(args.root_domain, args.output_dir)
    if output_path:
        print(f"Retrieved logo saved as {output_path}")
    else:
        print("Logo stored but failed to retrieve.")

if __name__ == '__main__':
    main()

