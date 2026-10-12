# v0.15 Hygiene + Shortcut Audit

## Scope
Based on v0.14 preserving all Reference Library and Model Adapter Registry, plus new Chinese type pipeline and case evidence.

## Existing dangerous shortcut closed
- Font family by name → verified local path + specific TTC face + file hash + cmap coverage.
- Correct CJK glyphs assumed beautiful → separate visual design assessment.
- Regular Songti called identical to custom glyph → custom-display flag and RED if mismatch.
- font-weight and CSS scale substitute for appropriate font file → forbidden.
- Browser checks `document.fonts.check` alone → insufficient; verify declared loaded font face and coverage separately.
- CJK vertical text treated as ordinary CSS paragraph → per-glyph design and actual proof required.

## Limitations / not falsely certified
- Browser cannot reliably prove every glyph was drawn from a single face without detailed shaping internals; use fontTools coverage together with browser loaded evidence. Some complex shaping may still need human inspection.
- `fontTools` cmap verifies mapping, not aesthetic quality; proof must be compared with Lead reference.
- No actual LoRA was downloaded/benchmarked in this revision.
- Exact font CSS files for the user-supplied failed screenshot are unavailable; actual cause of font fallback unknown.
- No third-party font binary is redistributed in this ZIP.

## Verification (this build)
- Reference Library entries: 113; readable image assets: 145; unreadable images: 0.
- JSON parsed: 25; YAML parsed: 60.
- Symbolic links, nested archives, bytecode caches, model weights, and hidden OS artifacts flagged: 0.
- `unittest` regression: 14 PASS (v0.14 intake + LoRA gates; v0.15 font file/glyph region/proof).
- Browser QA smoke test: PASS with actual local DejaVu custom face, and intentional wrong-family test correctly returned FAIL. This is a font-**loading** test, not an aesthetic-judgement test.
- Browser test used in-memory local asset inlining because this sandbox's Chromium disallows direct file navigation; scripts do not download external dependencies.
- Final ZIP will be verified with `testzip` separately.
