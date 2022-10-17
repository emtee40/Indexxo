<script setup lang="ts">
import { nextTick, onMounted, Ref, ref } from 'vue';

const props = defineProps<{
  onInputChange: ((newText: string) => void),
  inputText: string
}>()

const filter = ref<HTMLElement>();
const localInputText = ref(props.inputText)

onMounted(() => {
  nextTick(() => {
    filter.value?.focus();
  });
});

function keyUpAction() {
  props.onInputChange(localInputText.value)
}

function updateInput(event: Event) {
  localInputText.value = (event.target as HTMLInputElement).value
}

function clearInput() {
  localInputText.value = ""
}

</script>
    
<template>
  <div class="flex bg-white rounded-full p-3 m-4 mt-2 gap-3">
    <img src="/assets/icon_search.svg" alt="menu" @click="">
    <input ref="filter" class="text-md w-full flex-auto focus:outline-none" :value="localInputText" @input="updateInput"
      @keyup.enter="keyUpAction" placeholder="123 Search by names and paths">
    <img src="/assets/icon_close.svg" alt="menu" @click="clearInput">
  </div>
</template>
