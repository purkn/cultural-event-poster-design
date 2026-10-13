import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from reference_library import ingest, query, read, rebuild


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'library'
        self.source = Path(self.temp.name) / 'source'
        self.source.mkdir()

    def poster(self, name, color='red'):
        Image.new('RGB', (40, 60), color).save(self.source / name)

    def test_idempotent_import_and_annotation_preserved(self):
        self.poster('REF-001_市集_自由拼贴_手写_蓝黄.jpg')
        ingest(self.source, 'batch-one', self.root)
        manifest = self.root / 'collections/batch-one/manifest.json'
        data = read(manifest)
        data['references'][0]['observation_note'] = 'Reviewed locally'
        manifest.write_text(json.dumps(data))
        ingest(self.source, 'batch-one', self.root)
        entries = read(self.root / 'index.json')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['observation_note'], 'Reviewed locally')
        self.assertEqual(entries[0]['id'], 'batch-one:REF-001')

    def test_conflicting_artwork_does_not_overwrite(self):
        name = 'REF-001_市集_自由拼贴_手写_蓝黄.jpg'
        self.poster(name)
        ingest(self.source, 'batch-one', self.root)
        before = (self.root / 'index.json').read_bytes()
        self.poster(name, 'blue')
        with self.assertRaisesRegex(ValueError, 'ID conflict'):
            ingest(self.source, 'batch-one', self.root)
        self.assertEqual((self.root / 'index.json').read_bytes(), before)

    def test_duplicate_ids_and_malformed_names_fail_before_copy(self):
        self.poster('REF-001_市集_自由拼贴_手写_蓝黄.jpg')
        self.poster('REF-001_市集_自由拼贴_手写_蓝黄.png')
        with self.assertRaisesRegex(ValueError, 'Duplicate source ID'):
            ingest(self.source, 'batch-one', self.root)
        self.assertFalse((self.root / 'collections').exists())

    def test_cross_collection_dedup_and_unknown_queue(self):
        self.poster('REF-001_未知_自由拼贴_未知_未知.jpg')
        ingest(self.source, 'batch-one', self.root)
        report = ingest(self.source, 'batch-two', self.root)
        self.assertEqual(report['unique_images'], 1)
        self.assertEqual(report['duplicate_images'], 1)
        entries = read(self.root / 'index.json')
        self.assertEqual(len(query(entries, {'composition': '自由拼贴'})), 1)
        self.assertEqual(len(read(self.root / 'review_queue.json')), 2)
        self.assertEqual(entries[0]['strong_lead_eligible'], 'visual_review_required')

    def test_integrity_rejects_modified_asset(self):
        self.poster('REF-001_市集_自由拼贴_手写_蓝黄.jpg')
        ingest(self.source, 'batch-one', self.root)
        entry = read(self.root / 'index.json')[0]
        (self.root / entry['image_path']).write_bytes(b'broken')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            rebuild(self.root)

    def test_corrupt_existing_library_blocks_new_batch_before_copy(self):
        self.poster('REF-001_市集_自由拼贴_手写_蓝黄.jpg')
        ingest(self.source, 'batch-one', self.root)
        entry = read(self.root / 'index.json')[0]
        (self.root / entry['image_path']).write_bytes(b'broken')
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            ingest(self.source, 'batch-two', self.root)
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
    def test_alias_survives_removing_duplicate_asset_and_manifest(self):
        self.poster('REF-001_市集_自由拼贴_手写_蓝黄.jpg')
        ingest(self.source, 'batch-one', self.root)
        ingest(self.source, 'batch-two', self.root)
        import shutil
        shutil.rmtree(self.root / 'collections/batch-two')
        coverage = rebuild(self.root)
        self.assertEqual(coverage['total_images'], 1)
        self.assertEqual(read(self.root / 'aliases.json'), {'batch-two:REF-001': 'batch-one:REF-001'})
        rebuild(self.root)
        self.assertEqual(read(self.root / 'aliases.json'), {'batch-two:REF-001': 'batch-one:REF-001'})

    def test_invalid_alias_blocks_rebuild_before_index_write(self):
        self.poster('REF-001_市集_自由拼贴_手写_蓝黄.jpg')
        ingest(self.source, 'batch-one', self.root)
        before = (self.root / 'index.json').read_bytes()
        (self.root / 'aliases.json').write_text(json.dumps({'old': 'missing'}))
        with self.assertRaisesRegex(ValueError, 'Invalid reference alias'):
            rebuild(self.root)
        self.assertEqual((self.root / 'index.json').read_bytes(), before)

    def test_composition_precedes_event_semantics(self):
        self.poster('REF-001_市集_中心轴对称_衬线_蓝黄.jpg')
        self.poster('REF-002_艺术展览_自由拼贴_手写_蓝白.jpg', 'blue')
        ingest(self.source, 'batch-one', self.root)
        ranked = query(read(self.root / 'index.json'), {'event_type': '市集', 'composition': '自由拼贴'})
        self.assertTrue(ranked[0]['id'].endswith('REF-002'))

    def test_keyword_record_wins_over_untagged_legacy_alias(self):
        self.poster('REF-001_市集_自由拼贴_手写_蓝黄.jpg')
        ingest(self.source, 'batch-one', self.root)
        canonical = read(self.root / 'index.json')[0]
        legacy = dict(canonical, id='REF-001', collection='legacy-v013', metadata_source='legacy_provisional_clusters')
        for field in ('event_type', 'composition', 'typography', 'palette'):
            legacy.pop(field)
        manifest = self.root / 'collections/legacy-v013/manifest.json'
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({'references': [legacy]}))
        rebuild(self.root)
        self.assertEqual(read(self.root / 'aliases.json'), {'REF-001': 'batch-one:REF-001'})
        self.assertEqual(query(read(self.root / 'index.json'), {'event_type': '市集'})[0]['id'], 'batch-one:REF-001')


if __name__ == '__main__':
    unittest.main()
