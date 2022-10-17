<script setup lang="ts">
import { formatBytes, formatDate } from '../common/format-helpers';
import { FileObject } from '../common/FileObject';
import FileExplorerListItemGeneric from './FileExplorerListItemGeneric.vue';

const props = defineProps<{
  fileobj: FileObject
}
>()

const imgSrc = (() => {
  switch (props.fileobj.type) {
    case "archive": return "/assets/archive.svg";
    case "audio": return "/assets/audio.svg";
    case "document": return "/assets/document.svg";
    case "folder": return "/assets/folder.svg";
    case "image": return "/assets/image.svg";
    case "program": return "/assets/program.svg";
    case "space": return "/assets/space.svg";
    case "video": return "/assets/video.svg";

    default: return "/assets/other.svg";
  }
})();

const imgAlt = props.fileobj.type
const supportText = `${formatDate(new Date(props.fileobj.mtime * 1000))} • ${formatBytes(props.fileobj.size, 2)}`

</script>

<template>
  <FileExplorerListItemGeneric :img-src="imgSrc" :img-alt="imgAlt" :title="fileobj.full_name" :support="supportText" />
</template>
