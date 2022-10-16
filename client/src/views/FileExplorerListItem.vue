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
    case "archive": return "/src/assets/archive.svg";
    case "audio": return "/src/assets/audio.svg";
    case "document": return "/src/assets/document.svg";
    case "folder": return "/src/assets/folder.svg";
    case "image": return "/src/assets/image.svg";
    case "program": return "/src/assets/program.svg";
    case "space": return "/src/assets/space.svg";
    case "video": return "/src/assets/video.svg";

    default: return "/src/assets/other.svg";
  }
})();

const imgAlt = props.fileobj.type
const supportText = `${formatDate(new Date(props.fileobj.mtime * 1000))} • ${formatBytes(props.fileobj.size, 2)}`

</script>

<template>
  <FileExplorerListItemGeneric :img-src="imgSrc" :img-alt="imgAlt" :title="fileobj.full_name" :support="supportText" />
</template>
