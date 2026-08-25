<script setup>
defineProps({
  pipeline: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="pipeline-logs">
    <!-- 1. Preprocessing Log -->
    <div v-if="pipeline.preprocessing" class="pl-block">
      <div class="pl-header">
        <span class="pl-badge pl-badge--gray">Step 1</span>
        <span class="pl-title">Preprocessing & Tokenisasi</span>
        <span class="pl-meta">{{ pipeline.preprocessing.total_tokens }} Token BM25</span>
      </div>
      <div class="pl-content">
        <div class="pl-row">
          <span class="pl-label">Raw Query:</span>
          <span class="pl-val">"{{ pipeline.preprocessing.raw_query }}"</span>
        </div>
        <div class="pl-row" v-if="pipeline.preprocessing.final_tokens?.length">
          <span class="pl-label">Tokens BM25:</span>
          <div class="pl-tags">
            <span v-for="tok in pipeline.preprocessing.final_tokens" :key="tok" class="pl-tag">{{ tok }}</span>
          </div>
        </div>
        <div class="pl-row" v-if="pipeline.preprocessing.bigrams?.length">
          <span class="pl-label">N-Grams (Bigrams):</span>
          <div class="pl-tags">
            <span v-for="bg in pipeline.preprocessing.bigrams" :key="bg" class="pl-tag pl-tag--blue">{{ bg }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 2. Ekspansi Sinonim Log -->
    <div v-if="pipeline.ekspansi" class="pl-block">
      <div class="pl-header">
        <span class="pl-badge pl-badge--yellow">Step 2</span>
        <span class="pl-title">Ekspansi Ontologi Kata Kunci</span>
        <span class="pl-meta">{{ pipeline.ekspansi.num_frasa_ditemukan }} Frasa Cocok</span>
      </div>
      <div class="pl-content">
        <div v-if="pipeline.ekspansi.num_frasa_ditemukan > 0" class="pl-ekspansi-grid">
          <div v-for="(syn, phrase) in pipeline.ekspansi.log" :key="phrase" class="pl-ekspansi-item">
            <span class="pl-phrase">{{ phrase }}</span>
            <span class="pl-arrow">→</span>
            <span class="pl-syn">{{ syn }}</span>
          </div>
        </div>
        <div v-else class="pl-empty">Tidak ada kata kunci yang memicu ekspansi ontologi otomatis.</div>
      </div>
    </div>

    <!-- 3. BM25 Lexical Candidates -->
    <div v-if="pipeline.bm25" class="pl-block">
      <div class="pl-header">
        <span class="pl-badge pl-badge--blue">Step 3</span>
        <span class="pl-title">BM25 Lexical Filtering (Hard Constraint)</span>
        <span class="pl-meta">{{ pipeline.bm25.num_candidates }} / {{ pipeline.bm25.num_total_dosen }} Lolos</span>
      </div>
      <div class="pl-content">
        <div class="pl-candidates-list">
          <div v-for="(cand, idx) in pipeline.bm25.top_candidates" :key="idx" class="pl-cand-item">
            <span class="pl-cand-name">{{ cand.nama }}</span>
            <span class="pl-cand-score dc-score-box--blue">{{ cand.skor }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 4. SBERT Semantic Candidates -->
    <div v-if="pipeline.sbert" class="pl-block">
      <div class="pl-header">
        <span class="pl-badge pl-badge--fuchsia">Step 4</span>
        <span class="pl-title">Sentence-BERT Semantic Cosine Similarity</span>
        <span class="pl-meta">{{ pipeline.sbert.num_computed }} Dihitung</span>
      </div>
      <div class="pl-content">
        <div class="pl-candidates-list">
          <div v-for="(cand, idx) in pipeline.sbert.top_candidates" :key="idx" class="pl-cand-item">
            <span class="pl-cand-name">{{ cand.nama }}</span>
            <span class="pl-cand-score dc-score-box--fuchsia">{{ cand.skor }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 5. Hybrid Aggregation -->
    <div v-if="pipeline.hybrid" class="pl-block pl-block--highlight">
      <div class="pl-header">
        <span class="pl-badge pl-badge--brand">Step 5</span>
        <span class="pl-title">Hybrid Scoring & Adaptive Weighting</span>
        <span class="pl-meta">Mode: {{ pipeline.hybrid.mode }}</span>
      </div>
      <div class="pl-content">
        <div class="pl-weight-cards">
          <div class="pl-weight-card pl-weight-card--blue">
            <div class="pl-weight-label">α (BM25 Weight)</div>
            <div class="pl-weight-val">{{ pipeline.hybrid.alpha }}</div>
          </div>
          <div class="pl-weight-card pl-weight-card--fuchsia">
            <div class="pl-weight-label">β (SBERT Weight)</div>
            <div class="pl-weight-val">{{ pipeline.hybrid.beta }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pipeline-logs {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.pl-block {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.85rem;
}
.pl-block--highlight {
  border-color: var(--brand-dim);
  background: var(--brand-light);
}

.pl-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.pl-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-primary);
}
.pl-meta {
  margin-left: auto;
  font-size: 0.7rem;
  font-weight: 600;
  font-family: var(--font-mono);
  color: var(--text-muted);
}

.pl-badge {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
}
.pl-badge--gray { background: var(--bg-muted); color: var(--text-secondary); }
.pl-badge--yellow { background: #fef9c3; color: #a16207; }
.pl-badge--blue { background: var(--blue-bg); color: var(--blue); }
.pl-badge--fuchsia { background: var(--fuchsia-bg); color: var(--fuchsia); }
.pl-badge--brand { background: var(--brand); color: white; }

.pl-content {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.78rem;
}

.pl-row {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}
.pl-label {
  font-weight: 600;
  color: var(--text-muted);
  flex-shrink: 0;
}
.pl-val {
  font-family: var(--font-mono);
  color: var(--text-primary);
}

.pl-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.pl-tag {
  background: var(--bg-muted);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.72rem;
}
.pl-tag--blue {
  background: var(--blue-bg);
  color: var(--blue);
}

.pl-ekspansi-grid {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.pl-ekspansi-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--bg-subtle);
  padding: 0.35rem 0.5rem;
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.72rem;
}
.pl-phrase { font-weight: 700; color: var(--brand); }
.pl-arrow { color: var(--text-muted); }
.pl-syn { color: var(--text-secondary); }
.pl-empty { color: var(--text-muted); font-style: italic; font-size: 0.75rem; }

.pl-candidates-list {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.pl-cand-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.3rem 0.5rem;
  background: var(--bg-subtle);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
}
.pl-cand-name { font-weight: 600; color: var(--text-primary); }
.pl-cand-score {
  font-family: var(--font-mono);
  font-weight: 700;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}

.pl-weight-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}
.pl-weight-card {
  padding: 0.5rem;
  border-radius: var(--radius);
  text-align: center;
}
.pl-weight-card--blue { background: var(--blue-bg); }
.pl-weight-card--fuchsia { background: var(--fuchsia-bg); }
.pl-weight-label { font-size: 0.7rem; font-weight: 600; color: var(--text-muted); }
.pl-weight-val { font-size: 1.1rem; font-weight: 800; font-family: var(--font-mono); margin-top: 0.2rem; }
.pl-weight-card--blue .pl-weight-val { color: var(--blue); }
.pl-weight-card--fuchsia .pl-weight-val { color: var(--fuchsia); }
</style>
