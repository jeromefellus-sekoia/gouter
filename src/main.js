import { createApp, reactive } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { App } from "./App";
import { Login } from "./Login";
import { Index } from "./Index"

export const UI = reactive({
})

export const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: Index },
        { path: '/login', component: Login }
    ]
})

createApp(App).use(router).mount("body")