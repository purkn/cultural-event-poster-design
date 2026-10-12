#!/usr/bin/env python3
"""Audit actual HTML @font-face load for H0 in local Chromium and save screenshot.
Requires: playwright python + installed Chromium. No network access needed for local HTML.
"""
import argparse,json,sys,shutil,re,base64,mimetypes
from urllib.parse import urlparse,unquote
from pathlib import Path

def _asset_data_url(raw, base_dir):
    uri=raw.strip().strip('"\'')
    if uri.startswith(('data:', 'http:', 'https:', '#')):return uri
    parsed=urlparse(uri)
    if parsed.scheme not in ('', 'file'):return uri
    path=Path(unquote(parsed.path)) if parsed.scheme=='file' else base_dir/uri
    path=path.resolve()
    if not path.is_file():return uri
    mime=mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')

def _inline_css_urls(css, base_dir):
    return re.sub(r'url\(\s*([\"\']?)([^\)\"\']+)\1\s*\)',
                  lambda m:'url("'+_asset_data_url(m.group(2),base_dir)+'")',css,flags=re.IGNORECASE)

def _offline_html(html_path):
    """Offline proof only: inline local CSS/fonts/images, no remote fetching.
    Does not support JS-injected or remote CSS; audit must fail if selected face does not load.
    """
    target=Path(html_path).resolve()
    html=target.read_text(encoding='utf-8')
    def replace_link(m):
        tag=m.group(0)
        if not re.search(r'\brel\s*=\s*[\"\']stylesheet[\"\']',tag,re.I):return tag
        href=re.search(r'\bhref\s*=\s*[\"\']([^\"\']+)[\"\']',tag,re.I)
        if not href:return tag
        raw=href.group(1)
        cssfile=(target.parent/raw).resolve()
        if not cssfile.is_file():return tag
        content=_inline_css_urls(cssfile.read_text(encoding='utf-8'),cssfile.parent)
        return '<style>'+content+'</style>'
    html=re.sub(r'<link\b[^>]*>',replace_link,html,flags=re.I)
    html=_inline_css_urls(html,target.parent)
    def replace_img(m):
        tag=m.group(0)
        match=re.search(r'\bsrc\s*=\s*[\"\']([^\"\']+)[\"\']',tag,re.I)
        if not match:return tag
        val=_asset_data_url(match.group(1),target.parent)
        return tag[:match.start(1)]+val+tag[match.end(1):]
    html=re.sub(r'<img\b[^>]*>',replace_img,html,flags=re.I)
    return html

def audit(html_path, selector, expected_family, out_path, screenshot=None):
    from playwright.sync_api import sync_playwright
    target=Path(html_path).resolve()
    with sync_playwright() as p:
        try:
            browser=p.chromium.launch(headless=True)
        except Exception as first_error:
            exe=shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
            if not exe: raise RuntimeError('No Playwright-managed or system Chromium found; browser QA is UNVERIFIED') from first_error
            browser=p.chromium.launch(headless=True,executable_path=exe,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1200,'height':1500},device_scale_factor=1)
        page.set_content(_offline_html(target),wait_until='load')
        page.evaluate('document.fonts.ready')
        page.locator(selector).first.wait_for(state='visible')
        result=page.evaluate("""({selector, expected}) => {
          const el=document.querySelector(selector);if(!el)return {error:'selector not found'};
          const s=getComputedStyle(el);const fam=s.fontFamily;const synthesis=s.fontSynthesis;
          const faces=[...document.fonts].map(f=>({family:f.family,style:f.style,weight:f.weight,status:f.status}));
          const clean=x=>x.replace(/["']/g,'').trim().toLowerCase();
          const exp=clean(expected);
          const selected=fam.split(',').some(x=>clean(x)===exp);
          const loaded=faces.some(x=>clean(x.family)===exp && x.status==='loaded');
          const rect=el.getBoundingClientRect();
          const parent=el.closest('.poster')||document.body;
          const outer=parent.getBoundingClientRect();
          const inBounds=rect.left>=outer.left-1&&rect.right<=outer.right+1&&rect.top>=outer.top-1&&rect.bottom<=outer.bottom+1;
          return {text:el.textContent,fontFamilyComputed:fam,fontSynthesis:synthesis,expectedFamily:expected,faceDeclaredLoaded:loaded,familySelected:selected,faces,rect:{x:rect.x,y:rect.y,width:rect.width,height:rect.height},inPosterBounds:inBounds,scrollOverflow:el.scrollHeight>el.clientHeight+2||el.scrollWidth>el.clientWidth+2,imagesReady:[...document.images].every(i=>i.complete&&i.naturalWidth>0)};
        }""",{'selector':selector,'expected':expected_family})
        if screenshot:page.screenshot(path=str(Path(screenshot).resolve()),full_page=True)
        browser.close()
    if 'error' not in result:
        result['status']='PASS_FONT_LOAD' if (result['faceDeclaredLoaded'] and result['familySelected'] and result['fontSynthesis']=='none' and result['imagesReady'] and result['inPosterBounds'] and not result['scrollOverflow']) else 'FAIL_FONT_LOAD_OR_LAYOUT'
        result['caveat']='Offline proof uses local CSS/font/image assets inlined in browser memory; external/JS assets are unsupported. Browser face + cmap check are both needed to exclude fallback. This does not prove aesthetic fidelity.'
    Path(out_path).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--html',required=True);ap.add_argument('--selector',default='.h0');ap.add_argument('--expected-family',required=True);ap.add_argument('--out',required=True);ap.add_argument('--screenshot')
    a=ap.parse_args()
    try:r=audit(a.html,a.selector,a.expected_family,a.out,a.screenshot)
    except Exception as exc:print(json.dumps({'status':'ERROR','error':str(exc)},ensure_ascii=False));return 2
    print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r.get('status')=='PASS_FONT_LOAD' else 1
if __name__=='__main__':sys.exit(main())
