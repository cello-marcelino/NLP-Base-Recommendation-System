<script setup>
defineProps({
  index: Number,
  dosen: Object,
  scores: Object,
  xai: Object
})
</script>

<template>
  <tr class="dc-tr" :class="{ 'dc-tr--top': index === 0 }" @click="$emit('click')">
    <!-- Rank -->
    <td class="dc-td dc-td--center">
      <span v-if="index === 0" class="dc-rank dc-rank--top">1</span>
      <span v-else class="dc-rank">{{ index + 1 }}</span>
    </td>

    <!-- Nama -->
    <td class="dc-td">
      <div class="dc-name">{{ dosen.nama }}</div>
      <div class="dc-kata">
        Kata: {{ xai?.irisan_kata?.join(', ') || '-' }}
      </div>
    </td>

    <!-- Prodi -->
    <td class="dc-td">
      <div class="dc-prodi">{{ dosen.program_studi }}</div>
    </td>

    <!-- BM25 -->
    <td class="dc-td dc-td--center dc-score-box dc-score-box--blue">
      <div class="dc-score-val">{{ scores.bm25.toFixed(3) }}</div>
      <div class="dc-score-pct">{{ Math.round(scores.bm25 * 100) }}%</div>
    </td>

    <!-- SBERT -->
    <td class="dc-td dc-td--center dc-score-box dc-score-box--fuchsia">
      <div class="dc-score-val">{{ scores.sbert.toFixed(3) }}</div>
      <div class="dc-score-pct">{{ Math.round(scores.sbert * 100) }}%</div>
    </td>

    <!-- Hybrid -->
    <td class="dc-td dc-td--center dc-score-box dc-score-box--brand">
      <div class="dc-score-val">{{ scores.hybrid.toFixed(3) }}</div>
      <div class="dc-bar-wrap">
        <div class="dc-bar-fill" :style="`width: ${Math.round(scores.hybrid * 100)}%`"></div>
      </div>
    </td>
  </tr>
</template>

<style scoped>
.dc-tr {
  cursor: pointer;
  transition: background 0.15s;
  border-bottom: 1px solid var(--border);
}
.dc-tr:last-child { border-bottom: none; }
.dc-tr:hover { background: var(--bg-muted); }
.dc-tr--top { background: var(--brand-light); }
.dc-tr--top:hover { background: #e0d8ff; }

.dc-td {
  padding: 0.85rem 0.75rem;
  vertical-align: middle;
}
.dc-td--center { text-align: center; }

.dc-rank {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-muted);
}
.dc-rank--top {
  display: inline-flex; align-items: center; justify-content: center;
  width: 20px; height: 20px;
  background: var(--brand); color: white;
  border-radius: 50%;
}

.dc-name { font-size: 0.875rem; font-weight: 600; color: var(--text-primary); }
.dc-kata {
  font-family: var(--font-mono);
  font-size: 0.68rem; color: var(--blue);
  margin-top: 0.25rem;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 140px;
}

.dc-prodi { font-size: 0.75rem; color: var(--text-secondary); }

.dc-score-box { background: var(--bg-subtle); }
.dc-score-box--blue { background: var(--blue-bg); }
.dc-score-box--fuchsia { background: var(--fuchsia-bg); }
.dc-score-box--brand { background: var(--brand-light); }

.dc-score-val { font-family: var(--font-mono); font-size: 0.825rem; font-weight: 700; }
.dc-score-box--blue .dc-score-val { color: var(--blue); }
.dc-score-box--fuchsia .dc-score-val { color: var(--fuchsia); }
.dc-score-box--brand .dc-score-val { color: var(--brand); }

.dc-score-pct { font-family: var(--font-mono); font-size: 0.65rem; font-weight: 600; }
.dc-score-box--blue .dc-score-pct { color: #60a5fa; }
.dc-score-box--fuchsia .dc-score-pct { color: #e879f9; }

.dc-bar-wrap {
  width: 100%; height: 4px;
  background: rgba(91, 75, 219, 0.2);
  border-radius: 99px; overflow: hidden;
  margin-top: 4px;
}
.dc-bar-fill { height: 100%; background: var(--brand); border-radius: 99px; }
</style>
