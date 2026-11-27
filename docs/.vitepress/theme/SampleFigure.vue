<script setup lang="ts">
import { withBase } from 'vitepress'

/** File names in samples/. The label is the last part of each name. */
const files = [
  'sample_01_merbc',
  'sample_02_tkcdv',
  'sample_03_rhecf',
  'sample_04_mjufv',
  'sample_05_drguf',
  'sample_06_aefeu',
  'sample_07_fhfsv',
  'sample_08_jebvh',
  'sample_09_btffj',
  'sample_10_zhcab',
]

const props = withDefaults(defineProps<{ limit?: number }>(), { limit: 10 })

const rows = files.slice(0, props.limit).map((file, i) => ({
  n: String(i + 1).padStart(2, '0'),
  src: withBase(`/samples/${file}.jpg`),
  label: file.split('_')[2],
}))
</script>

<template>
  <table class="samples">
    <thead>
      <tr>
        <th scope="col" class="n">No.</th>
        <th scope="col">Input image, 200 x 50</th>
        <th scope="col">Label</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="r in rows" :key="r.n">
        <td class="n">{{ r.n }}</td>
        <td class="img">
          <img :src="r.src" width="200" height="50" :alt="`E-captcha sample image labelled ${r.label}`" loading="lazy" />
        </td>
        <td class="label">{{ r.label }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.samples {
  display: table;
  width: 100%;
  margin: 0;
  border-collapse: collapse;
  border-top: 1.5px solid var(--ec-rule-strong);
  border-bottom: 1.5px solid var(--ec-rule-strong);
}
.samples th,
.samples td {
  border: 0;
  background: none;
  padding: 0.38rem 0;
  text-align: left;
  vertical-align: middle;
}
.samples tr {
  background: none;
  border: 0;
}
.samples th {
  padding: 0.45rem 0;
  border-bottom: 1px solid var(--ec-rule-strong);
  font-size: 0.9rem;
  font-weight: 600;
}
.samples tbody td {
  border-top: 1px solid var(--ec-rule);
}
.samples tbody tr:first-child td {
  border-top: 0;
}
.n {
  width: 3.2rem;
  font-family: var(--ec-mono);
  font-size: 0.8rem;
  color: var(--ec-ink-3);
}
.samples th.n {
  font-family: var(--ec-serif);
  font-size: 0.9rem;
  color: inherit;
}
.img img {
  display: block;
  width: 200px;
  max-width: 100%;
  height: auto;
}
.label {
  width: 6.5rem;
  padding-left: 1rem !important;
  font-family: var(--ec-mono);
  font-size: 1.12rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  color: var(--ec-accent);
}
.samples th:last-child {
  padding-left: 1rem;
}
@media (max-width: 420px) {
  .n {
    width: 2.4rem;
  }
  .label {
    width: 5.4rem;
    font-size: 1rem;
    letter-spacing: 0.1em;
  }
}
</style>
