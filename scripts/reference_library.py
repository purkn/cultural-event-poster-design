#!/usr/bin/env python3
"""Import keyword-named posters, rebuild facets/previews, and retrieve candidates."""
import argparse
import csv
import hashlib
import html
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1] / 'reference_library'
FACETS = ('event_type', 'composition', 'typography', 'palette')
PATTERN = re.compile(r'^(REF-\d+)_(.+?)_(.+?)_(.+?)_(.+)$')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_info(path):
    with Image.open(path) as image:
        image.load()
        width, height = ImageOps.exif_transpose(image).size
    return {'width': width, 'height': height, 'aspect': round(width / height, 4)}


def ingest(source, collection, root=ROOT):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', collection):
        raise ValueError('Collection must be a lowercase slug')
    source = Path(source)
    files = sorted(p for p in source.iterdir() if p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'})
    if not files:
        raise ValueError('No supported images found')
    manifest = root / 'collections' / collection / 'manifest.json'
    existing = read(manifest) if manifest.exists() else {'collection': collection, 'references': []}
    entries = {entry['id']: entry for entry in existing['references']}
    pending = []
    seen = set()
    # Validate the complete incoming batch before copying any assets.
    for path in files:
        match = PATTERN.fullmatch(path.stem)
        if not match:
            raise ValueError(f'Expected REF-NNN_event_composition_typography_palette: {path.name}')
        source_id, *tags = match.groups()
        ref_id = f'{collection}:{source_id}'
        if ref_id in seen:
            raise ValueError(f'Duplicate source ID: {source_id}')
        seen.add(ref_id)
        sha = digest(path)
        if ref_id in entries and entries[ref_id]['sha256'] != sha:
            raise ValueError(f'ID conflict: {ref_id}; use a new collection for different artwork')
        if ref_id in entries:
            continue  # Stable identity, including any later visual annotations.
        target = Path('collections') / collection / 'images' / path.name
        entry = {
            'id': ref_id, 'source_id': source_id, 'collection': collection,
            'image_path': target.as_posix(), 'original_name': path.name,
            'source_path': f'{source.name}/{path.name}', 'sha256': sha,
            **image_info(path), **dict(zip(FACETS, tags)),
            'metadata_source': 'filename_keywords', 'metadata_status': 'provisional',
            'visual_review_status': 'pending', 'status': 'raw_reference',
            'role_hint': 'unassigned', 'strong_lead_eligible': 'visual_review_required',
            'needs_review': '未知' in tags,
        }
        pending.append((path, target, entry))
    for path, target, entry in pending:
        (root / target).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, root / target)
        entries[entry['id']] = entry
    existing['references'] = sorted(entries.values(), key=lambda entry: entry['id'])
    existing['metadata_source'] = 'filename_keywords'
    write(manifest, existing)
    return rebuild(root)


def rebuild(root=ROOT):
    entries = []
    for manifest in sorted((root / 'collections').glob('*/manifest.json')):
        entries.extend(read(manifest)['references'])
    # Prefer keyword-tagged records as canonical, while preserving all legacy IDs.
    entries.sort(key=lambda entry: (entry.get('metadata_source') != 'filename_keywords', entry['id']))
    ids = set()
    hashes = {}
    facets = {field: defaultdict(list) for field in FACETS}
    for entry in entries:
        if entry['id'] in ids:
            raise ValueError(f"Duplicate ID: {entry['id']}")
        ids.add(entry['id'])
        path = root / entry['image_path']
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Asset outside library: {path}')
        sha = digest(path)
        if entry.get('sha256') != sha:
            raise ValueError(f'Asset checksum mismatch: {path}')
        if image_info(path) != {key: entry[key] for key in ('width', 'height', 'aspect')}:
            raise ValueError(f'Image dimensions mismatch: {path}')
        entry.pop('duplicate_of', None)
        if sha in hashes:
            entry['duplicate_of'] = hashes[sha]
        else:
            hashes[sha] = entry['id']
        for field in FACETS:
            if entry.get(field):
                facets[field][entry[field]].append(entry['id'])
    write(root / 'index.json', entries)
    columns = sorted({key for entry in entries for key in entry})
    with (root / 'index.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(entries)
    write(root / 'facets.json', facets)
    write(root / 'aliases.json', {entry['id']: entry['duplicate_of'] for entry in entries if entry.get('duplicate_of')})
    write(root / 'review_queue.json', [entry['id'] for entry in entries if entry.get('needs_review')])
    coverage = {
        'total_images': len(entries), 'unique_images': len(hashes),
        'duplicate_images': len(entries) - len(hashes),
        'collections': dict(Counter(entry['collection'] for entry in entries)),
        'facets': {field: {tag: len(refs) for tag, refs in values.items()} for field, values in facets.items()},
        'unknown_tag_images': sum(bool(entry.get('needs_review')) for entry in entries),
        'coverage_basis': 'inventory_and_provisional_tags_not_visual_style_maturity',
    }
    write(root / 'coverage.json', coverage)
    return coverage


def query(entries, terms, top=12):
    """Keyword shortlist only; score is never a fine visual-fit or Lead score."""
    ranked = []
    for entry in entries:
        if entry.get('duplicate_of'):
            continue
        matched = [field for field, term in terms.items() if term and term in entry.get(field, '')]
        if terms and not matched:
            continue
        score = sum({'composition': 4, 'typography': 3, 'palette': 2, 'event_type': 1}[field] for field in matched)
        ranked.append({**entry, 'keyword_score': score, 'matched_fields': matched})
    return sorted(ranked, key=lambda entry: (-entry['keyword_score'], entry['id']))[:top]


def previews(root=ROOT):
    entries = [entry for entry in read(root / 'index.json') if not entry.get('duplicate_of')]
    output = root / 'previews'
    output.mkdir(exist_ok=True)
    pages = []
    # Paginated contact sheets: stable IDs on each tile; full tags in the gallery.
    for offset in range(0, len(entries), 40):
        canvas = Image.new('RGB', (1000, 1600), 'white')
        draw = ImageDraw.Draw(canvas)
        for tile, entry in enumerate(entries[offset:offset + 40]):
            x, y = tile % 5 * 200, tile // 5 * 200
            with Image.open(root / entry['image_path']) as source:
                thumb = ImageOps.exif_transpose(source).convert('RGB')
                thumb.thumbnail((184, 166))
                canvas.paste(thumb, (x + (200 - thumb.width) // 2, y + 4))
            label = entry['id'].replace('keyword-20261012:', 'KW:')
            draw.text((x + 5, y + 175), label, fill='black')
        filename = f'contact-{offset // 40 + 1:03}.jpg'
        canvas.save(output / filename, quality=85)
        pages.append(filename)
    for old in output.glob('contact-*.jpg'):
        if old.name not in pages:
            old.unlink()
    write(output / 'manifest.json', {'page_size': 40, 'total_images': len(entries), 'pages': pages})
    cards = []
    for entry in entries:
        tags = ' / '.join(entry.get(field, '') for field in FACETS)
        path = html.escape('../' + entry['image_path'], quote=True)
        cards.append(f'<article><a href="{path}"><img loading="lazy" src="{path}" alt="{html.escape(entry["id"])}"></a><b>{html.escape(entry["id"])}</b><p>{html.escape(tags or entry.get("cluster_initial", ""))}</p></article>')
    (output / 'gallery.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>参考海报索引</title><style>body{font-family:system-ui;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:20px}img{width:100%;height:250px;object-fit:contain}b,p{font-size:12px;overflow-wrap:anywhere}</style><h1>参考海报索引</h1><p>标签待视觉确认；浏览器查找可检索关键词。点击查看原图。</p><main>' + ''.join(cards) + '</main></html>', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    importer = sub.add_parser('import')
    importer.add_argument('source', type=Path)
    importer.add_argument('--collection', required=True)
    sub.add_parser('rebuild')
    sub.add_parser('previews')
    search = sub.add_parser('query')
    for field in FACETS:
        search.add_argument('--' + field.replace('_', '-'))
    search.add_argument('--top', type=int, default=12)
    args = parser.parse_args()
    if args.command == 'import':
        print(json.dumps(ingest(args.source, args.collection), ensure_ascii=False, indent=2))
    elif args.command == 'rebuild':
        print(json.dumps(rebuild(), ensure_ascii=False, indent=2))
    elif args.command == 'previews':
        previews()
    else:
        if args.top < 1:
            parser.error('--top must be positive')
        terms = {field: getattr(args, field) for field in FACETS if getattr(args, field)}
        print(json.dumps(query(read(ROOT / 'index.json'), terms, args.top), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
