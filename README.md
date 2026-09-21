# Keagan's Kodaks

Cut one photo into a seamless Instagram carousel, on your phone.

**Open it:** https://kfillies.github.io/keagan-s-kodak-

Then in Safari tap **Share**, **Add to Home Screen**, **Add**. It gets its own
icon, opens full screen, works offline, and never expires.

## What it does

Pick a wide photo and it splits across the carousel so the seams disappear
when someone swipes.

- Suggests a slide count from the photo's own shape, adjustable from 2 to 10.
- 4:5, 1:1 and 9:16, the three shapes Instagram accepts.
- Drag to reposition, pinch to zoom. In Fill mode the drag is bounded so the
  photo can never expose the background, which is the most common way a
  carousel comes out wrong.
- Warns before you export when the source is too narrow to hold the width.
- Renders each slide at 1080px and hands them to the iOS share sheet, where
  "Save N Images" puts them in your library numbered in upload order.

## Design

Built to iOS conventions: SF Pro straight off the device on Apple's type scale,
inset grouped list rows with hairline separators, segmented controls whose
thumb slides on a critically damped spring, an iOS stepper, and translucent
blurred bars. Colours are Apple's published system values, assigned by role, so
light and dark both come from one set of tokens.

Appearance follows the phone by default, with an explicit System / Light / Dark
override on the start screen that is remembered between visits. The icon has
its own dark cut, because a near-white plate glares against a black ground.

No webfont, so it renders correctly on a first launch with no signal.

## Verified

Driven headless at iPhone viewport with a 3600px test panorama. Concatenating
the exported slides reproduces the full canvas with a worst-case seam
discontinuity of **0**, so the split is pixel-exact.

## Layout

```
index.html            the whole app: markup, styles, logic
manifest.webmanifest  name, icons, standalone display
sw.js                 offline cache
icons/                home screen icons, light and dark, plus their generator
```

Run it locally with `python3 -m http.server 4173`. Saving to Photos needs a
real device; a desktop browser falls back to downloading each slide.

## Where the rest lives

There is a macOS companion, a full continuous-canvas carousel editor, in the
private ReadRoute repository under `KeagansKodaks/`.
