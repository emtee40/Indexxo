<script setup lang="ts">
import MenuVue from './Menu.vue';
defineProps<{
    titleText: string
    supportText?: string
}>()

function openMenu() {
    const menu = document.getElementById("menu")
    menu?.classList.remove("hidden")
    menu?.classList.add("visible")
}

function closeMenu() {
    const menu = document.getElementById("menu")
    menu?.classList.add("hidden")
    menu?.classList.remove("visible")
}

</script>

<template>
    <div class="relative">
        <MenuVue class="fixed hidden" id="menu" :close-me-action="closeMenu" />
        <div class="p-3">
            <div class="flex">
                <p class="text-xl text-white font-bold flex-auto">{{titleText}}</p>
                <img src="/assets/icon_menu.svg" alt="menu" @click="openMenu">
            </div>
            <p class="text-lg text-white">{{supportText}}</p>
        </div>
    </div>
</template>
