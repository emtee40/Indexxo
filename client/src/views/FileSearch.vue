<script setup lang="ts">
import MainHeader from './MainHeader.vue';
import FileSearchBar from './FileSearchBar.vue';
import FileExplorerListItem from './FileExplorerListItem.vue';
import { ref } from 'vue';
import { FileObject } from '../common/FileObject';
import { useRoute, useRouter } from 'vue-router';

const latestContent = ref<FileObject[]>([])
const loading = ref(false)
const router = useRouter()
const route = useRoute()
const currentInputText = ref((route.query.searchQuery || "").toString())

// Load results only when there there is something in search bar
if (currentInputText.value.length > 0) {
    loadResults()
}

function clearTextField() {
    currentInputText.value = ""
}

function onInputChange(newInput: string) {
    router.push({ name: "FileSearch", query: { searchQuery: newInput } })
}

function loadResults() {
    loading.value = true
    fetch('http://127.0.0.1:5000/search?query=' + currentInputText.value)
        .then((response) => response.json())
        .then((data) => {
            latestContent.value = data.result
            loading.value = false
        })
        .catch((error) => console.log(error))
}

function clickItem(item: FileObject) {
    if (!["folder", "space"].includes(item.type)) return alert("i am a file!")
    router.push({ name: "FileExplorer", query: { path: item.full_path } })
}

</script>
        
<template>
    <div class="flex flex-col h-screen main-gradient">
        <MainHeader title-text="File Search"></MainHeader>
        <FileSearchBar :clear-action=clearTextField :on-input-change=onInputChange :input-text=currentInputText>
        </FileSearchBar>
        <div class="flex flex-grow flex-col bg-bottom bg-white pt-4 pb-16 rounded-t-3xl">
            <div v-if="loading" class="m-auto grid place-items-center gap-8">
                <img class="object-contain h-48" src="/src/assets/undraw_searching.svg" alt="menu">
                <div class="text-sm">Loading...</div>
            </div>
            <div v-else-if="route.query.searchQuery === undefined" class="m-auto grid place-items-center gap-8">
                <img class="object-contain h-48" src="/src/assets/undraw_search_initial.svg" alt="menu">
                <div class="text-sm">Search for anything</div>
            </div>
            <div v-else-if="latestContent.length == 0" class="m-auto grid place-items-center gap-8">
                <img class="object-contain h-48" src="/src/assets/undraw_void.svg" alt="menu">
                <div class="text-sm">No results</div>
            </div>
            <div v-else v-for="item in latestContent" :key="item.full_path" @click="clickItem(item)">
                <FileExplorerListItem :fileobj="item" />
            </div>
        </div>
    </div>
</template>
