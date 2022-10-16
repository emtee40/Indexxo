<script setup lang="ts">

defineProps<{
    imgSrc: string,
    imgAlt: string,
    title: string,
    support?: string
}
>()

</script>
    
<template>
    <div class="px-3 py-2 hover:bg-gray-200 rounded-2xl">
        <div class="flex items-center">
            <img :src="imgSrc" :alt="imgAlt">
            <div class="ml-4">
                <p>{{title}}</p>
                <p class="text-sm">{{support}}</p>
            </div>
        </div>
    </div>
</template>
