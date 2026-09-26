#!/usr/bin/env python3
"""Collect Changi route/airline headlines from free news feeds into news.json.

Run once a day by .github/workflows/news.yml (no AI, no keys). Keeps what it
found on earlier days, so the list builds up even though each feed only shows
its last few stories. The map's Insights page reads news.json when it opens.
"""
import json, re, html, urllib.request, email.utils
from datetime import datetime, timedelta, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

FEEDS = [
    ('CNA', 'https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=10416'),
    ('Mainly Miles', 'https://mainlymiles.com/feed/'),
    ('AeroRoutes', 'https://aeroroutes.com/eng?format=rss'),
    ('AeroTime', 'https://www.aerotime.aero/feed'),
    ('Business Traveller', 'https://www.businesstraveller.com/feed/'),
    ('TTG Asia', 'https://www.ttgasia.com/feed/'),
    ('Aviation A2Z', 'https://aviationa2z.com/index.php/feed/'),
    ('Straits Times', 'https://www.straitstimes.com/news/singapore/rss.xml'),
    ('Straits Times', 'https://www.straitstimes.com/news/business/rss.xml'),
    ('Business Times', 'https://www.businesstimes.com.sg/rss/transport'),
    ('The Edge Singapore', 'https://www.theedgesingapore.com/rss.xml'),
    ('FlightGlobal', 'https://www.flightglobal.com/rss'),
]
# the headline must name Singapore/Changi AND be about flying; judged on the headline only
PLACE = re.compile(r'\b(changi|singapore|scoot|sia)\b', re.I)
AVIA = re.compile(r'\b(scoot|passengers?|airlines?|flights?|routes?|airports?|terminals?|carriers?|aircraft|jets?|aviation|air travel|levy)\b', re.I)
SKIP = re.compile(r'\b(krisflyer|miles|points|credit card|citi|lounge|award|sale|promo\w*|deals?|review|seats?|cabins?|first class|business class|priority pass|mro|prison|jail|court|charged|crash\w*|collid\w*|drugs?|smuggl\w*|arrested|beach)\b', re.I)
def wanted(title): return bool(PLACE.search(title) and AVIA.search(title) and not SKIP.search(title))
COUNTRIES = {'China': r'china|chinese|beijing|shanghai|guangzhou|shenzhen|chengdu|xiamen|hangzhou|urumqi|hohhot',
             'Hong Kong': r'hong kong|macau', 'Japan': r'japan|tokyo|osaka|nagoya|fukuoka|sapporo|okinawa',
             'South Korea': r'korea|seoul|busan|jeju', 'Thailand': r'thailand|thai|bangkok|phuket|chiang mai|krabi',
             'Malaysia': r'malaysia|kuala lumpur|penang|sabah|sarawak|johor|langkawi', 'Indonesia': r'indonesia|jakarta|bali|surabaya|medan|batam|aceh',
             'Philippines': r'philippine|manila|cebu|clark|davao', 'Vietnam': r'vietnam|hanoi|ho chi minh|da nang|hai phong|da lat|phu quoc'}
KEEP_DAYS, KEEP_MAX = 120, 40
OUT = Path(__file__).parent / 'news.json'

def text(el, tag):
    x = el.find(tag)
    return html.unescape(re.sub(r'<[^>]+>', ' ', x.text or '')).strip() if x is not None and x.text else ''

def fetch(name, url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (changi-routes news bot)'})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
    for it in root.iter('item'):
        title, link, desc = text(it, 'title'), text(it, 'link'), text(it, 'description')[:600]
        try: when = email.utils.parsedate_to_datetime(text(it, 'pubDate')).astimezone(timezone.utc)
        except Exception: when = datetime.now(timezone.utc)
        blob = f'{title} {desc}'
        if not wanted(title):
            continue
        tags = [c for c, rx in COUNTRIES.items() if re.search(rx, blob, re.I)]
        yield {'title': title, 'url': link, 'src': name, 'date': when.strftime('%Y-%m-%d'), 'tags': tags}

old = [i for i in (json.loads(OUT.read_text())['items'] if OUT.exists() else []) if wanted(i['title'])]   # re-check old ones when the rules change
seen = {i['url'] for i in old}
new = []
for name, url in FEEDS:
    try:
        for item in fetch(name, url):
            if item['url'] not in seen:
                seen.add(item['url']); new.append(item)
    except Exception as e:   # one broken feed never stops the rest
        print(f'skip {name}: {e}')
cut = (datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)).strftime('%Y-%m-%d')
items = sorted([i for i in old + new if i['date'] >= cut], key=lambda i: i['date'], reverse=True)[:KEEP_MAX]
OUT.write_text(json.dumps({'updated': datetime.now(timezone.utc).strftime('%Y-%m-%d'), 'items': items}, ensure_ascii=False, indent=1))
print(f'{len(new)} new, {len(items)} kept')
