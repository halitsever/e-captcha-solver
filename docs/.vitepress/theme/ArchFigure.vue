<script setup lang="ts">
import { withBase } from 'vitepress'

/** Shapes follow CRNN.forward in model_ctc.py for a 1 x 50 x 200 input. */
const stages = [
  { kind: 'image', w: 200, h: 50, title: 'Input', detail: 'grayscale, scaled to [-1, 1]', shape: '1 × 50 × 200' },
  { kind: 'map', w: 100, h: 25, title: 'Conv block 1', detail: '1 → 32 channels, pool 2 × 2', shape: '32 × 25 × 100' },
  { kind: 'map', w: 50, h: 12, title: 'Conv block 2', detail: '32 → 64 channels, pool 2 × 2', shape: '64 × 12 × 50' },
  { kind: 'map', w: 50, h: 6, title: 'Conv block 3', detail: '64 → 128 channels, pool 2 × 1', shape: '128 × 6 × 50' },
  { kind: 'map', w: 50, h: 3, title: 'Conv block 4', detail: '128 → 256 channels, pool 2 × 1', shape: '256 × 3 × 50' },
  { kind: 'map', w: 50, h: 1, title: 'Conv block 5', detail: '256 → 256 channels, pool 3 × 1', shape: '256 × 1 × 50' },
  { kind: 'seq', w: 120, h: 12, title: 'Squeeze and permute', detail: 'width becomes 50 time steps', shape: '50 × 256' },
  { kind: 'rnn', w: 120, h: 30, title: 'Bidirectional LSTM', detail: '2 layers, 256 hidden, dropout 0.2', shape: '50 × 512' },
  { kind: 'grid', w: 120, h: 30, title: 'Linear', detail: '512 → 20 classes per step', shape: '50 × 20' },
  { kind: 'text', w: 120, h: 26, title: 'Greedy CTC decode', detail: 'argmax, collapse, drop blanks', shape: '5 letters' },
]

/** One scale for the image and every feature map, so their proportions are true. */
const k = 0.6
const pitch = 62
const cx = 62
const rows = stages.map((s, i) => {
  const scaled = s.kind === 'image' || s.kind === 'map'
  const w = scaled ? s.w * k : s.w
  const h = scaled ? s.h * k : s.h
  const mid = 30 + i * pitch
  return { ...s, w, h, mid, x: cx - w / 2, y: mid - h / 2 }
})
const height = 30 + (stages.length - 1) * pitch + 30
const links = rows.slice(0, -1).map((r, i) => ({ y1: r.y + r.h, y2: rows[i + 1].y }))
const sample = withBase('/samples/sample_01_merbc.jpg')
</script>

<template>
  <div class="arch-scroll">
    <svg
      class="arch"
      :viewBox="`0 0 470 ${height}`"
      role="img"
      aria-label="Architecture of the CRNN: a 200 by 50 grayscale image passes through five convolutional blocks that reduce the height to 1 and the width to 50, then a two-layer bidirectional LSTM with 256 hidden units, then a linear layer that outputs 20 classes for each of 50 time steps, decoded greedily into five letters."
    >
      <defs>
        <pattern id="arch-cells" width="2.4" height="1.5" patternUnits="userSpaceOnUse">
          <path d="M2.4 0V1.5M0 1.5H2.4" class="cell" />
        </pattern>
        <pattern id="arch-steps" width="2.4" height="12" patternUnits="userSpaceOnUse">
          <rect x="0.4" y="0" width="1.6" height="12" class="step" />
        </pattern>
      </defs>

      <line v-for="(l, i) in links" :key="`l${i}`" :x1="cx" :x2="cx" :y1="l.y1" :y2="l.y2" class="flow" />

      <g v-for="(r, i) in rows" :key="i">
        <template v-if="r.kind === 'image'">
          <image :href="sample" :x="r.x" :y="r.y" :width="r.w" :height="r.h" preserveAspectRatio="none" />
          <rect :x="r.x" :y="r.y" :width="r.w" :height="r.h" class="frame" />
        </template>
        <rect v-else-if="r.kind === 'map'" :x="r.x" :y="r.y" :width="r.w" :height="Math.max(r.h, 1.4)" class="map" />
        <rect v-else-if="r.kind === 'seq'" :x="r.x" :y="r.y" :width="r.w" :height="r.h" fill="url(#arch-steps)" />
        <template v-else-if="r.kind === 'rnn'">
          <rect :x="r.x + 4" :y="r.y + 4" :width="r.w" :height="r.h" class="box back" />
          <rect :x="r.x" :y="r.y" :width="r.w" :height="r.h" class="box" />
          <path :d="`M${r.x + 12} ${r.mid - 6}H${r.x + r.w - 13}m-6 -3.5l6 3.5l-6 3.5`" class="arrow" />
          <path :d="`M${r.x + r.w - 12} ${r.mid + 6}H${r.x + 13}m6 -3.5l-6 3.5l6 3.5`" class="arrow" />
        </template>
        <template v-else-if="r.kind === 'grid'">
          <rect :x="r.x" :y="r.y" :width="r.w" :height="r.h" class="box" />
          <rect :x="r.x" :y="r.y" :width="r.w" :height="1.5" class="blank" />
          <rect :x="r.x" :y="r.y" :width="r.w" :height="r.h" fill="url(#arch-cells)" />
        </template>
        <text v-else :x="cx" :y="r.mid + 8" text-anchor="middle" class="out">merbc</text>

        <text x="146" :y="r.mid - 3" class="title">{{ r.title }}</text>
        <text x="146" :y="r.mid + 15" class="detail">{{ r.detail }}</text>
        <text x="470" :y="r.mid - 3" text-anchor="end" class="shape">{{ r.shape }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.arch-scroll {
  overflow-x: auto;
}
.arch {
  display: block;
  width: 100%;
  max-width: 560px;
  height: auto;
}
.flow {
  stroke: var(--ec-ink);
  stroke-width: 1;
}
.frame {
  fill: none;
  stroke: var(--ec-ink);
  stroke-width: 1;
}
.map {
  fill: var(--ec-accent);
}
.step {
  fill: var(--ec-accent);
}
.box {
  fill: var(--ec-sheet);
  stroke: var(--ec-ink);
  stroke-width: 1;
}
.box.back {
  fill: var(--ec-wash);
}
.arrow {
  fill: none;
  stroke: var(--ec-accent);
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.cell {
  fill: none;
  stroke: var(--ec-rule);
  stroke-width: 0.4;
}
.blank {
  fill: var(--ec-accent);
  opacity: 0.35;
}
.title {
  font-family: var(--ec-serif);
  font-size: 16px;
  font-weight: 600;
  fill: var(--ec-ink);
}
.detail {
  font-family: var(--ec-mono);
  font-size: 11.5px;
  fill: var(--ec-ink-2);
}
.shape {
  font-family: var(--ec-mono);
  font-size: 12.5px;
  font-weight: 500;
  fill: var(--ec-ink);
}
.out {
  font-family: var(--ec-mono);
  font-size: 21px;
  font-weight: 500;
  letter-spacing: 0.12em;
  fill: var(--ec-accent);
}
</style>
