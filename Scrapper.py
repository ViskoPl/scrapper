import sys
import urllib2
import smtplib
import time
import io
# web library
import httplib
import datetime
from bs4 import BeautifulSoup
from email.utils import COMMASPACE, formatdate
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

POSTS = []
FILE = open('log.txt', 'r+')
connection = httplib.HTTPSConnection("discordapp.com")
URL = "https://discordapp.com/api/webhooks/608477939725500416/rFRsG7n3eTHY5Ub7GDoSz02P3dvBWOwYdRjxVDIyl8DwJiAUNDhdbNB8-1FrNfTYeZZq"


class Post:

    def __init__(self, link="", title="", description_main='', published_date='', price_eur='', price_hrk='',
                 post_id=""):
        self.link = link
        self.title = title
        self.description_main = description_main
        self.published_date = published_date
        self.price_eur = price_eur
        self.price_hrk = price_hrk
        self.post_id = post_id

    def __str__(self):
        return "Link: {}  Title: {}  | Description {} | Cijena_kune: {} id: {} \n".format(self.link.encode("utf-8"), self.title.encode("utf-8"),
                                                                                          self.description_main.encode(
                                                                                              "utf-8"),
                                                                                          self.price_hrk.encode(
                                                                                              "utf-8"),
                                                                                          self.post_id.encode("utf-8"))


def createRequest(url):
    request = urllib2.Request(url)
    request.add_header('authority', "www.njuskalo.hr")
    request.add_header('method', "GET")
    request.add_header('scheme', "https")
    # request.add_header('cookie', "__uzma=905a2bf2-a6ad-4a6d-88c4-7d7f359fa6cd; __uzmb=1531318031; njupop=cf103f3429f6ffd510434497d368c8f2130a292e42cfdfeeedeaadc0ba6e167a; xtvrn=$413863$; _STUU=27b0f755-fe70-4ed7-b569-9910f31ba9ad; __gfp_64b=mrYllu_VOT_2zVXFXcC0KKFzCNB3CbDpPJSh0Aq4VlD.E7; _ga=GA1.2.559398381.1531318032; njuskalo_privacy_policy=4; njuskalo_adblock_detected=true; PHPSESSID=519309f3846cd148edcc4d22b68a24b3; __utmc=228389250; DM_SitId220=true; DM_SitId220SecId924=true; comm100_guid2_1000306=NwLkq08vdUi4V5jrv5dvCw; DM_SitId220SecId922=true; DM_SitId220SecId931=true; DM_SitId220SecId943=true; __uzmaj2=; __uzmbj2=; DM_SitId220SecId923=true; _gid=GA1.2.181095487.1537091623; njuskalo_accept_cookies=true; DM_SitId220SecId925=true; __utmz=228389250.1537187983.135.13.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __ssuzjsr2=a9be2cd8e; __uzmc=72517922976411; uzdbm_a=cdb6f8be-851d-e41d-980f-c91ae28f34e2; __uzmd=1537200462; __utma=228389250.559398381.1531318032.1537198431.1537200464.138; __utmt=1; __utmb=228389250.1.10.1537200464; __uzmcj2=215861090433; __uzmdj2=1537200464; DM_SitIdT220=true; DM_SitId220SecIdT924=true; ccapi.accessTokenUserId=-1; ccapi.accessToken=1015ac6d6f1e81ce45f0a623ecd4085b5b1180c4b3ac5e40d6003cc6109877660a9128e94c73586db08d94daee50a211b8fcf3dfecfa2590785ee7a3ee640b24ba7637fe2dc33d8a84812674ea950a8e; _dc_gtm_UA-2376274-8=1; DotMetricsTimeOnPage=")
    request.add_header('user-agent',
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36")
    return request


def fill_new_posts(posts):
    new_posts = []
    with io.open('log.txt', 'r', encoding='utf8') as f:
        f.seek(0)
        ids_date = f.read().split('\n')
        ids_date = [x for x in ids_date if x]

    for post in posts:
        new_post = create_post(post)
        if new_post is None:
            continue
        if len(ids_date) == 0 or all(
                (new_post.post_id != item.split('-')[0])
                for item in ids_date):
            try:
                with io.open('log.txt', 'a', encoding='utf8') as f:
                    f.write(new_post.post_id + '-' + new_post.published_date +
                            '| title:' + new_post.title + '\n')

            except Exception as e:
                print('Something went wrong...' + str(e))
            new_posts.append(new_post)
    return new_posts


def create_post(post):
    link = ''
    title = ''
    description = ''
    date = ''
    price_hrk = ''
    price_eur = ''
    post_id = ''
    if post.find('a', attrs={'class': 'link'}):
        link = "https://www.njuskalo.hr" + \
            post.find('a', attrs={'class': 'link'})['href']
        post_id = post.find('a', attrs={'class': 'link'})[
            'href'].split('/')[2].split('-')[-1]
    if post.find('a', attrs={'class': 'link'}):
        title = post.find('a', attrs={'class': 'link'}).text
    if post.find('div', attrs={'class': 'entity-description-main'}):
        description = post.find(
            'div', attrs={'class': 'entity-description-main'}).text.strip()
    if post.find('time', attrs={'class': 'date'}):
        date = post.find('time', attrs={'class': 'date'}).text
    if post.find('strong', attrs={'class': 'price price--hrk'}):
        price_hrk = post.find(
            'strong', attrs={'class': 'price price--hrk'}).text
    if post.find('strong', attrs={'class': 'price price--eur'}):
        price_eur = post.find(
            'strong', attrs={'class': 'price price--eur'}).text

    if date and link and title and price_hrk and post_id:
        return Post(link, title, description, date, price_eur, price_hrk, post_id)
    else:
        return None


def main():
    while True:
        new_posts = []
        # go onto the https://njuskalo.www to get the link with your desired filters
        url = "https://www.njuskalo.hr/iznajmljivanje-stanova?locationIds=1261%2C1262%2C1263%2C1255%2C1253&price%5Bmax%5D=600&flatBuildingType=flat-in-residential-building"
        request = createRequest(url)
        page = urllib2.urlopen(request)
        print("Sending requset to the site----------------")
        soup = BeautifulSoup(page, 'html.parser', from_encoding="utf-8")
        posts = soup.findAll('li', attrs={'class': 'EntityList-item'})
        print("Oppening soup ---------------")
        new_posts = fill_new_posts(posts)
        print("Issuing a requst at {}".format(datetime.datetime.now()))
        if new_posts:
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login(username_email, password)
                sent_from = username_email
                msg = MIMEMultipart("alternative")
                msg['From'] = username_email
                msg['To'] = COMMASPACE.join(EMAILS)
                msg['Date'] = formatdate(localtime=True)
                msg['Subject'] = 'Novi oglasi'
                text = ""
                counter = 1
                for post in new_posts:
                    text += str(post) + '\n'
                    send(text)
                    msg.attach(MIMEText(text, "plain",  "utf-8"))
                    if counter % 10 == 0:
                        # server.sendmail(sent_from, EMAILS, msg.as_string().encode('ascii'))
                        msg['body'] = ''
                        text = ""
                    counter += 1
                    time.sleep(1)
                if len(new_posts) % 10 != 0:
                    print "asdadasd"
                   #  server.sendmail(sent_from, EMAILS, msg.as_string().encode('ascii'))
                server.close()
                print("Posts sent")
            except Exception as e:
                print('Something went wrong...'+str(e))
        time.sleep(900)


def send(text):

    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + \
        text + "\r\n------:::BOUNDARY:::--"

    # get the response
    connection.request("POST", URL, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
    })
    response = connection.getresponse()
    result = response.read()

    # return back to the calling function with the result
    return result.decode("utf-8")


if __name__ == "__main__":
    main()
