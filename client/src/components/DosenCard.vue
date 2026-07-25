<template>
  <tr :class="['hover:bg-surface-50 transition-colors font-mono', index === 0 ? 'bg-primary-50/50' : '']"
      style="cursor: pointer;">
    <td class="p-3 text-center">
      <span v-if="index === 0" class="text-xs font-extrabold bg-primary-500 text-white rounded-full w-6 h-6 inline-flex items-center justify-center">1</span>
      <span v-else class="text-surface-400 font-bold text-xs">{{ index + 1 }}</span>
    </td>
    <td class="p-3">
      <div class="font-bold text-surface-800 font-sans text-sm">{{ dosen.NAMA }}</div>
      <div v-if="dosen['Irisan Kata (Lexical)'] && dosen['Irisan Kata (Lexical)'] !== '-'"
        class="text-[9px] text-blue-500 mt-0.5 truncate max-w-40">
        Kata: {{ dosen['Irisan Kata (Lexical)'].substring(0, 40) }}{{ dosen['Irisan Kata (Lexical)'].length > 40 ? '...' : '' }}
      </div>
    </td>
    <td class="p-3">
      <div class="text-[10px] text-surface-500 font-sans">{{ dosen.PROGRAM_STUDI }}</div>
    </td>
    <td class="p-3 text-center text-blue-600 font-bold bg-blue-50/30">
      <div>{{ dosen['Lexical Score'] }}</div>
      <div class="text-[9px] text-blue-400">{{ Math.round(dosen['Lexical Score'] * 100) }}%</div>
    </td>
    <td class="p-3 text-center text-fuchsia-600 font-bold bg-fuchsia-50/30">
      <div>{{ dosen['Semantic Score'] }}</div>
      <div class="text-[9px] text-fuchsia-400">{{ Math.round(dosen['Semantic Score'] * 100) }}%</div>
    </td>
    <td class="p-3 text-center bg-primary-50">
      <div class="text-primary-700 font-extrabold">{{ dosen['Hybrid Score'] }}</div>
      <div class="w-full bg-primary-100 rounded-full h-1.5 mt-1 overflow-hidden">
        <div class="bg-primary-500 h-1.5 rounded-full" :style="`width: ${Math.round(dosen['Hybrid Score'] * 100)}%`"></div>
      </div>
    </td>
  </tr>
</template>

<script setup>
defineProps({
  dosen: Object,
  index: Number
});
</script>
