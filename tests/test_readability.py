from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
_test_dir=tempfile.TemporaryDirectory(prefix='poster-readability-')
tmp=Path(_test_dir.name)
script=root/'scripts/check_text_readability.py'
bg=Image.new('RGB',(300,200),'white');ImageDraw.Draw(bg).rectangle((0,0,95,199),fill='black');bg.save(tmp/'bg.png')
layer=Image.new('RGBA',bg.size,(0,0,0,0));d=ImageDraw.Draw(layer)
for x in [15,45,75]:d.rectangle((x,20,x+12,85),fill='white')
layer.save(tmp/'text.png')
fin=Image.alpha_composite(bg.convert('RGBA'),layer).convert('RGB');fin.save(tmp/'final.png')
b={'id':'h0','bbox':[0,0,280,140],'color':'#FFFFFF','font_px':64,'role':'h0'}
def run(name,expected,blocks=None,mask='text.png',final='final.png',scale='0.25'):
    (tmp/'blocks.json').write_text(json.dumps([b] if blocks is None else blocks))
    args=[sys.executable,str(script),'--background',str(tmp/'bg.png'),'--final',str(tmp/final),'--blocks',str(tmp/'blocks.json'),'--scale',scale]
    if mask:args+=['--text-layer',str(tmp/mask)]
    r=subprocess.run(args,capture_output=True,text=True)
    assert r.returncode==expected,(name,r.returncode,r.stdout,r.stderr)
    print(name,'PASS')
    return r
run('glyph contrast passes on busy bbox',0)
run('legacy conservative bbox still fails',1,mask=None)
run('empty blocks rejected',2,blocks=[])
run('invalid scale rejected',2,scale='nan')
run('missing text rejected',1,final='bg.png')
wrong=layer.copy();ImageDraw.Draw(wrong).rectangle((15,20,27,85),fill='red');wrong.save(tmp/'wrong.png')
run('unrelated glyph layer rejected',1,mask='wrong.png')
Image.new('RGBA',bg.size,'white').save(tmp/'opaque.png');run('opaque mask rejected',2,mask='opaque.png')
Image.new('RGBA',(20,20)).save(tmp/'small.png');run('wrong size mask rejected',2,mask='small.png')
Image.new('RGBA',bg.size).save(tmp/'empty.png');run('invisible glyph layer rejected',1,mask='empty.png')
run('off-canvas rejected',1,blocks=[dict(b,bbox=[-1,0,200,100])])
run('small type rejected',1,blocks=[dict(b,font_px=6)])
run('duplicate ids rejected',2,blocks=[b,b])
# Visible but dark ink on black must fail even with correct composition.
low=layer.copy();ld=ImageDraw.Draw(low)
for x in [15,45,75]:ld.rectangle((x,20,x+12,85),fill='#111111')
low.save(tmp/'low.png');Image.alpha_composite(bg.convert('RGBA'),low).convert('RGB').save(tmp/'low-final.png')
run('actual low contrast cannot hide behind metadata color',1,mask='low.png',final='low-final.png')

_test_dir.cleanup()
