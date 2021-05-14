import Vue from 'vue'
import VueRouter from 'vue-router'
import Report from './components/Report'
import Map from './components/Map'

Vue.use(VueRouter)


const routes = [
    { path: '/report', component: Report },
    { path: '/', component:  Map }
]

const router = new VueRouter({
    routes
})

export default router