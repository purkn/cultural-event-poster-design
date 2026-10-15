#!/usr/bin/env python3
"""Compose three real, same-canvas layers. Does not generate or split images."""
import argparse,base64,json
from pathlib import Path
from PIL import Image

def load_layers(hero,title,text):
    images=[]
    for path in (hero,title,text):
        with Image.open(path) as original: images.append(original.copy())
    if len({im.size for im in images})!=1:raise ValueError('all layers must share one canvas; no implicit resizing')
    for im in images:
        if 'A' not in im.getbands() and 'transparency' in im.info:raise ValueError('convert palette transparency to RGBA explicitly')
    for name,im in zip(('title','text'),images[1:]):
        if 'A' not in im.getbands():raise ValueError(name+' must have alpha')
        lo,hi=im.getchannel('A').getextrema()
        if lo==255 or hi==0:raise ValueError(name+' must be nonempty and transparent')
    if 'A' in images[0].getbands() and images[0].getchannel('A').getextrema()[0]<255:raise ValueError('hero must be composited onto its actual background')
    return [im.convert('RGBA') for im in images]

def compose(hero,title,text,project,language):
    if not language or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in language):raise ValueError('invalid language filename token')
    images=load_layers(hero,title,text);project=Path(project).resolve()
    paths=[f'01_final/poster_{language}.png',f'02_hero/hero_{language}.png',f'03_title/title_{language}.png',f'04_text/text_{language}.png',f'05_source/layers_{language}.svg',f'06_metadata/text_combined_{language}.png',f'06_metadata/composition_{language}.json']
    if any(not (project/p).resolve().is_relative_to(project) for p in paths):raise ValueError('output symlink escapes project')
    if any((project/p).exists() for p in paths):raise FileExistsError('use a new version/project; refusing to overwrite')
    for p in paths:(project/p).parent.mkdir(parents=True,exist_ok=True)
    final=Image.alpha_composite(Image.alpha_composite(images[0],images[1]),images[2]).convert('RGB')
    final.save(project/paths[0]);images[0].save(project/paths[1]);images[1].save(project/paths[2]);images[2].save(project/paths[3])
    Image.alpha_composite(images[1],images[2]).save(project/paths[5])
    w,h=images[0].size
    nodes=[]
    for label,p in zip(('hero','title','text'),paths[1:4]):
        data=base64.b64encode((project/p).read_bytes()).decode('ascii')
        nodes.append(f'<g id="{label}"><image width="{w}" height="{h}" href="data:image/png;base64,{data}"/></g>')
    (project/paths[4]).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><desc>Three embedded raster layers; not editable font outlines or live body text.</desc>'+''.join(nodes)+'</svg>',encoding='utf-8')
    (project/paths[6]).write_text(json.dumps({'canvas':[w,h],'language':language,'source_type':'embedded_raster_layers','editable_glyphs':False,'editable_body_text':False,'files':paths},ensure_ascii=False,indent=2),encoding='utf-8')
    return paths

def main():
    a=argparse.ArgumentParser();a.add_argument('--hero',required=True);a.add_argument('--title',required=True);a.add_argument('--text',required=True);a.add_argument('--project',required=True);a.add_argument('--language',required=True);args=a.parse_args()
    try:print(json.dumps(compose(args.hero,args.title,args.text,args.project,args.language),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as exc:a.exit(2,str(exc)+'\n')
if __name__=='__main__':main()
