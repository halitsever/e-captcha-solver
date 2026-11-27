<script setup lang="ts">
import { withBase } from 'vitepress'

/** Hand-written 50-step path for sample 09. It illustrates the rule and is not model output. */
const path = '------bbb-tt--fff-ff--jj' + '-'.repeat(26)

/** Same rule as greedy_decode in model_ctc.py: keep a class when it changes, then skip blanks. */
const collapsed: string[] = []
let prev = ''
for (const c of path) {
  if (c !== prev) collapsed.push(c)
  prev = c
}
const text = collapsed.filter((c) => c !== '-').join('')
const steps = [...path]
const sample = withBase('/samples/sample_09_btffj.jpg')
</script>

<template>
  <div class="ctc">
    <div class="scroll">
      <div class="strip">
        <svg class="input" viewBox="0 0 200 50" role="img" aria-label="Sample image labelled btffj with 50 time steps marked along its width, one every 4 pixels">
          <image :href="sample" width="200" height="50" />
          <path v-for="i in 49" :key="i" :d="`M${i * 4} 0V50`" class="tick" />
        </svg>
        <div class="cells" aria-hidden="true">
          <span v-for="(c, i) in steps" :key="i" :class="{ on: c !== '-' }">{{ c }}</span>
        </div>
      </div>
    </div>

    <ol class="rule">
      <li>
        <span class="what">Top class at each of the 50 steps</span>
        <code class="seq long">{{ path }}</code>
      </li>
      <li>
        <span class="what">Collapse repeats</span>
        <code class="seq"><span v-for="(c, i) in collapsed" :key="i" :class="{ on: c !== '-' }">{{ c }}</span></code>
      </li>
      <li>
        <span class="what">Drop blanks</span>
        <code class="seq result">{{ text }}</code>
      </li>
    </ol>
  </div>
</template>

<style scoped>
.scroll {
  overflow-x: auto;
}
.strip {
  min-width: 620px;
  max-width: 800px;
}
.input {
  display: block;
  width: 100%;
  height: auto;
  border: 1px solid var(--ec-ink);
  border-bottom: 0;
}
.tick {
  stroke: var(--ec-accent);
  stroke-width: 0.18;
  opacity: 0.55;
}
.cells {
  display: grid;
  grid-template-columns: repeat(50, 1fr);
  border: 1px solid var(--ec-ink);
}
.cells span {
  display: block;
  padding: 0.3rem 0;
  font-family: var(--ec-mono);
  font-size: 0.78rem;
  line-height: 1.2;
  text-align: center;
  color: var(--ec-ink-3);
  border-left: 1px solid var(--ec-rule);
}
.cells span:first-child {
  border-left: 0;
}
.cells span.on {
  background: var(--ec-accent);
  color: #fff;
  font-weight: 500;
  border-left-color: var(--ec-accent);
}

.rule {
  margin: 1.4rem 0 0;
  padding: 0;
  list-style: none;
  counter-reset: rule;
  border-top: 1px solid var(--ec-rule);
}
.rule li {
  counter-increment: rule;
  display: grid;
  grid-template-columns: 17.5rem 1fr;
  gap: 0.2rem 1.2rem;
  align-items: baseline;
  margin: 0;
  padding: 0.65rem 0;
  border-bottom: 1px solid var(--ec-rule);
}
.what {
  font-size: 1rem;
}
.what::before {
  content: counter(rule) '.';
  display: inline-block;
  width: 1.6rem;
  color: var(--ec-ink-3);
  font-variant-numeric: lining-nums;
}
.seq {
  padding: 0;
  background: none;
  font-family: var(--ec-mono);
  font-size: 0.86rem;
  color: var(--ec-ink-2);
  letter-spacing: 0.04em;
  overflow-wrap: anywhere;
}
.seq .on {
  color: var(--ec-accent);
  font-weight: 500;
}
.seq:not(.long):not(.result) span {
  margin-right: 0.45em;
}
.seq.result {
  font-size: 1.3rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  color: var(--ec-accent);
}
@media (max-width: 720px) {
  .rule li {
    grid-template-columns: 1fr;
  }
}
</style>
