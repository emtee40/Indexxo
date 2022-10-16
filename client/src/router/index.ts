import { createWebHistory, createRouter } from "vue-router"
import FileExplorer from "../views/FileExplorer.vue"
import FileSearch from "../views/FileSearch.vue"

const routes = [
    {
        path: "/",
        name: "FileExplorer",
        component: FileExplorer
    },
    {
        path: "/search",
        name: "FileSearch",
        component: FileSearch
    },
    {
        path: '/:catchAll(.*)*',
        redirect: { name: "FileExplorer" }
    },
]

const router = createRouter(
    {
        history: createWebHistory(),
        routes: routes
    }
)

export default router
