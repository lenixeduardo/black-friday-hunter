from pathlib import Path
from playwright.sync_api import sync_playwright
import mimetypes, json, time, re, base64
ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'app'
OUT=ROOT/'artifacts/amazon'
OUT.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    raw=(APP/'index.html').read_text('utf-8')
    def replace_asset(m):
        relative=m.group(1)
        asset=ROOT/relative.lstrip('/')
        if not asset.is_file():
            raise FileNotFoundError(relative)
        mime='image/webp' if asset.suffix=='.webp' else 'image/png' if asset.suffix=='.png' else 'image/svg+xml'
        return 'src="data:'+mime+';base64,'+base64.b64encode(asset.read_bytes()).decode('ascii')+'"'
    page_html=re.sub(r'src="(/app/[^"]+)"',replace_asset,raw)
    for w in (390,768,1440):
        page=browser.new_page(viewport={'width':w,'height':900},device_scale_factor=1,service_workers='block',reduced_motion='reduce')
        page.route('https://fonts.googleapis.com/**',lambda r:r.abort())
        page.route('https://fonts.gstatic.com/**',lambda r:r.abort())
        errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
        page.set_content(page_html,wait_until='domcontentloaded',timeout=10000)
        page.locator('#amazon-curadoria').wait_for()
        page.evaluate('''async()=>{await Promise.all([...document.querySelectorAll('.amazon-item img')].map(async x=>{x.loading='eager';await x.decode().catch(()=>{})}))}''')
        info=page.evaluate('''()=>({w:innerWidth,scroll:document.documentElement.scrollWidth, count:document.querySelectorAll('.amazon-item').length, amazonVisible:!!document.querySelector('#amazon-curadoria').offsetParent,images:[...document.querySelectorAll('.amazon-item img')].filter(x=>!x.complete||!x.naturalWidth).length, logoLoaded:document.querySelector('.brand')?.naturalWidth || 0})''')
        assert info['w']==w and info['count']==10 and info['images']==0,info
        if info['scroll']>w+2: print('OVERFLOW',w,page.evaluate('''()=>[...document.querySelectorAll('body *')].map(e=>({tag:e.tagName,cls:e.className?.baseVal||e.className,id:e.id,rect:e.getBoundingClientRect().right})).filter(x=>x.rect>innerWidth+2).slice(0,15)'''))
        assert info['scroll'] <=w+2,info
        assert info['amazonVisible'],info
        assert not errs,errs
        page.locator('#amazon-curadoria').scroll_into_view_if_needed()
        path=OUT/f'amazon-{w}.png'
        page.screenshot(path=str(path),full_page=True,animations='disabled')
        # All links should open exact submitted URL
        urls=page.eval_on_selector_all('.amazon-list-link','xs=>xs.map(x=>x.href)')
        assert all(x=='https://amzn.to/4846Sow' for x in urls)
        # Category toggling and search only once to save time
        if w==390:
            page.select_option('#interest','TECH')
            assert page.locator('#amazon-curadoria').is_hidden()
            page.select_option('#interest','TCG')
            assert page.locator('#amazon-curadoria').is_visible()
            page.locator('#search-form input').fill('Reinado Delta')
            page.locator('#search-form button').click()
            assert page.locator('.amazon-item:visible').count()==4, page.locator('.amazon-item:visible').count()
            page.locator('#search-form input').fill('')
            page.locator('#search-form button').click()
            assert page.locator('.amazon-item:visible').count()==10
        results.append({'width':w,'state':'PASS','info':info,'errors':errs,'screenshot':str(path)})
        page.close()
    browser.close()
(OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('BROWSER PASSED:',len(results),'screenshots', [x['screenshot'] for x in results])
