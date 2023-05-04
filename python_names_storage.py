from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "trans-sanctum-382223",
  "private_key_id": "c768f3c2cd22947efa11592318ae0d51b761ef77",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC/lUxRZgBDHzyA\niqqY9+JK/6giQTh9xWjiqHtUxi1HUV/yppBjTrNT6tZuzmLh/b4weowob+kvAXw/\nJ+E6C0ZEmJI4hPar6cty3Y4YycbbNJaSN/sOKe0UrGoD4vjJKljTyrtt2E2hSVhR\nNEDPeqEtbdPJBwnyTZWG8VVSrk5kHwgFdPpHCsBtMA9jkn5NG0gpp3OhzcasGBdr\ncjYUj13tnnKKZ+8Wmu6mBYknLs6EmX/zyBzTnmvn7dstmjdLSavjdUyeLZ4zoB5N\nSG8IzVRZipU9b2ym6jd4DraUydtoR+dup8WW+b1SKJwcb2MVDFzQUy1rxrf5Y4li\nMe6XKSwPAgMBAAECggEAAO7VebySR8Flwb3rIHi21tKodqkY7sGTDy5ckj8cz56r\nQTr12Hg97Zpm3zT6qAHu5JhmduY7eMCOhzFZGEnWVp6bAxwE736F92RfqsWFWGI2\nmqOuAZWmrsNgLVwYvOjnBmfc5vBSbit+sb+uiR1C56u6rJQ5DZsDr634CUGcCvlW\nH8dEjfwsWGpw1lIQbCdxcYoe4p4oIpIrTIbqG2fCwiCTLDH0yE5aWz7hsXWQ8ozh\nZWOBGGCspOMzaUvQKkoAq++zvUmNWf84G+T3FT196rgI8WxnV4H/K5w5594DgSYk\nmoyqofya1h71zm/LjElF88dcfLxWb6shPDMTdjIrIQKBgQDmWqPibg6UHJN3o+PR\nXUSLy8b8tBz3Hfnf3GoWuyQAa4T3sPUQZSnB+IAvPUZP+3C/SeWX/rRxghCYUsk8\n6GAtzEfVUxk9AscKJJ49YkAVNbCZUuLd0BAJ8AtJeYVp07+xpI7HE2gEFRWcXkQS\nqy5Pwy1Soh1ZurM/UVDFttTLiQKBgQDU6aSX37wxzR3D1EYHhOrEvvFQD+uQ3La6\nyCgofUdAfdJOdROpT9Cr9+4F/NZKpXytbOMMJVBKvCmRwRUFE3q2hOMC/X7lkDCK\n5nxCrLytNYmU/PMT1ndQOW2ytDLXjUBxvSk8GWFki55m5tNRuTG903xF9/ufVB8t\nf1OQ0qVc1wKBgFHq5eD+Fn0hdGfVhozLyDaWrxrqymou5M9xSODwiCsGEXEsItpD\nv4fVYXBrL/f9iOjd1KIq1+yNvm0M87ePQ7TFsr3wIUeLF1FKGGPn7rYcM8MysK8E\n8M836Cum5YTu4nq/9G5jPlhFTzweYcLp0TxYQmPiduGT/W6E8l59WEtRAoGAOoUB\nXVD8a//Bp5qHqPdqg6srrmLBz24qt0neZ8qPM/WhQTlCry2l4C5j+LdWuuujShN8\nkFENMY1oK4yTV3LULqh1sNO19ijcfsD89GJ/9Weaqh2gPhqbbqxqL00CEGbdiKWC\nWOds8nLBlezptjOdrVwccyrGuTMo4pt1f3+2Pb8CgYBA41UL9bNe438/HQTN3veT\n7/axYzeJuNmBcXGExaL+0w/f6d15qIgq2PHUy+eGleP6/lSx8BH4lcf35Jx1saiw\nwyNpfcXIihf8beBOsdBcPPVJeppfk0270GKq1Ot/7bIrFWSYJ/3i+IlnEOhdZoS2\nTRJS/S+nZj3LbrD9nXdvOA==\n-----END PRIVATE KEY-----\n",
  "client_email": "646374179998-compute@developer.gserviceaccount.com",
  "client_id": "105803026594360942955",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/646374179998-compute%40developer.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atv4z') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
