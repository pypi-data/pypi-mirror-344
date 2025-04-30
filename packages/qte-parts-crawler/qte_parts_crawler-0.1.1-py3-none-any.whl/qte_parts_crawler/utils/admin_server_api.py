import requests


ADMIN_SERVER_URL = "https://zmley-crawler-454529324517.us-central1.run.app"
POST_CRAWL_PREPARE_URL = ADMIN_SERVER_URL + "/crawlers/prepare"
POST_CRAWL_DETAIL_URL = ADMIN_SERVER_URL + "/crawlers/detail"

def get_prepare_tasks(count=3):
    """
    Fetches the list of tasks from the backend.
    """
    try:
        response = requests.get(url=POST_CRAWL_PREPARE_URL + f"?taskNumber={count}")
        if response.status_code == 200:
            return response.json()
        else:
            print('Error fetching tasks from backend:', response.status_code)
            return {}
    except Exception as e:
        print('Error fetching tasks from backend:', e)
        return {}


def post_crawl_prepare(year, make, model):
    data = {
        'year': str(year),
        'make': make,
        'model': model,
    }
    print('Posting crawl prepare to backend:', data)
    try:
        requests.post(url=POST_CRAWL_PREPARE_URL, json=data)
    except:
        print('Error posting crawl prepare to backend:', data)
        pass


def post_crawl_detail(year, make, model, part_type, engine, property_map):
    data = {
        'year': str(year),
        'make': make,
        'model': model,
        'partType': part_type,
        'engine': engine,
        'supplier': property_map['Supplier'],
        'partNumber': property_map['Part Number'],
        'comment': property_map['Comment'],
        'location': property_map['Location'],
        'brand': property_map['Brand'],
        'application': property_map['Application'],
        'qty': property_map['Qty'],
    }
    print('Posting crawl detail to backend:', data)
    try:
        requests.post(url=POST_CRAWL_DETAIL_URL, json=data)
    except:
        print('Error posting crawl detail to backend:', data)
        pass
