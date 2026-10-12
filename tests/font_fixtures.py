"""Local fonts for integration tests; overrides fail clearly when unavailable."""
import os
from pathlib import Path
from fontTools.ttLib import TTFont

def local_font(kind):
    candidates = {
        'cjk': ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/System/Library/Fonts/STHeiti Light.ttc'],
        'latin': ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'],
    }[kind]
    override = os.environ.get('POSTER_TEST_' + kind.upper() + '_FONT')
    for path in ([override] if override else candidates):
        if Path(path).is_file():
            face = int(os.environ.get('POSTER_TEST_' + kind.upper() + '_FACE', '2' if 'NotoSansCJK' in path else ('1' if 'STHeiti' in path else '0')))
            font = TTFont(path, fontNumber=face)
            family = font['name'].getDebugName(1)
            font.close()
            return path, face, family
    raise RuntimeError('Set POSTER_TEST_' + kind.upper() + '_FONT to a local font; integration tests require real fonts')
