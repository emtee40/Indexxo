<script setup lang="ts">
import { nextTick, onMounted, Ref, ref } from 'vue';

defineProps<{
  clearAction: (() => void),
  onInputChange: ((newText: string) => void),
  inputText: string
}>()

const filter = ref<HTMLElement>();

onMounted(() => {
  nextTick(() => {
    filter.value?.focus();
  });
});

</script>
    
<template>
  <div class="flex bg-white rounded-full p-3 m-4 mt-2 gap-3">
    <img src="/src/assets/icon_search.svg" alt="menu" @click="">
    <input ref="filter" class="text-md w-full flex-auto focus:outline-none" v-model="inputText"
      @keyup.enter="onInputChange(inputText)" placeholder="Search by names and paths">
    <img src="/src/assets/icon_close.svg" alt="menu" @click="clearAction">
  </div>
</template>
