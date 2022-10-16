<script setup lang="ts">
import { useRouter } from 'vue-router';

const props = defineProps<{
    closeMeAction: (() => void)
}>()

const router = useRouter()

function goTo(newRouteName: string) {
    props.closeMeAction()
    router.push({ name: newRouteName })
}

</script>
    
<template>
    <div class="flex h-screen w-screen bg-gray-400 main-gradient">
        <div class="m-auto">
            <p class="m-2 text-2xl text-white" @click="goTo('FileExplorer')">File Explorer</p>
            <p class="m-2 text-2xl text-white" @click="goTo('FileSearch')">File Search</p>
            <p class="m-2 text-2xl text-white" @click="goTo('Settings')">Settings</p>
            <p class="m-2 text-2xl text-white" @click="closeMeAction">Close menu</p>
        </div>
    </div>
</template>
