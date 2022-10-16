<script setup lang="ts">
import { ref } from 'vue';
import { FileObject } from '../common/FileObject';
import FileExplorerListItem from './FileExplorerListItem.vue';
import MainHeader from './MainHeader.vue';
import FileExplorerListItemGeneric from './FileExplorerListItemGeneric.vue';
import { useRoute, useRouter } from 'vue-router';
import { computed } from '@vue/reactivity';

const parentFileObject = ref<FileObject>()
const folderContent = ref<FileObject[]>([])
const showSpacesButton = ref(false)
const emptyFolder = ref(false)
const supportText = ref("My Spaces")
const router = useRouter()
const route = useRoute()
const path = computed(() => {
    return route.query.path?.toString() || ""
})

function loadContent(path: string = "") {
    fetch('http://127.0.0.1:5000/folder?path=' + path)
        .then((response) => response.json())
        .then((data) => {
            supportText.value = "Loading..."
            parentFileObject.value = data.parent
            folderContent.value = data.content
            emptyFolder.value = (folderContent.value.length === 0)
            /**
             * If no path is provided or we are not at the highest level of a space,
             * showSpaceButton is hidden. It's only visible when parent is undefined and we
             * are inside of a space
             */
            showSpacesButton.value = !(path === "" || parentFileObject.value != undefined)
            supportText.value = (path === "") ? "My spaces" : path
        })
        .catch((error) => console.log(error));
}

function clickListItem(item: FileObject) {
    if (['folder', 'space'].includes(item.type)) {
        // User clicked a folder or a space   
        router.push({ name: "FileExplorer", query: { path: item.full_path } })
    } else {
        // User clicked a file, can`t go deeper
        alert("Not implemented yet")
    }
}

function clickGoSpaces() {
    router.push({ name: "FileExplorer" })
}

function clickGoBack() {
    const parentPath = parentFileObject.value ? parentFileObject.value.full_path : ""
    router.push({ name: "FileExplorer", query: { path: parentPath } })
}

loadContent(path.value)

</script>

<template>
    <div class="flex flex-col h-screen main-gradient">
        <MainHeader title-text="File Explorer" :support-text="supportText" class=""></MainHeader>
        <div class="flex flex-grow flex-col bg-bottom bg-white pt-4 pb-16 rounded-t-3xl">
            <div v-if="parentFileObject" @click="clickGoBack()">
                <FileExplorerListItemGeneric img-src="./src/assets/back.svg" img-alt="Go up" title=".." />
            </div>
            <div v-else-if="showSpacesButton" @click="clickGoSpaces">
                <FileExplorerListItemGeneric img-src="./src/assets/back.svg" img-alt="Go to My Spaces"
                    title="Go back to My Spaces" />
            </div>
            <div v-if="emptyFolder" class="m-auto grid place-items-center gap-8">
                <img class="object-contain h-48" src="/src/assets/undraw_void.svg" alt="menu">
                <div class="text-sm">It's empty in here...</div>
            </div>
            <div v-else v-for="item in folderContent" :key="item.full_path" @click="clickListItem(item)">
                <FileExplorerListItem :fileobj="item" />
            </div>
        </div>
    </div>
</template>
