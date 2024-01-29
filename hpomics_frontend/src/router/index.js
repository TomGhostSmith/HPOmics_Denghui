import {createRouter, createWebHashHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SideBar from "@/components/workspace/GlobalComponent/SideBar.vue";
import NaviBar from "@/components/workspace/GlobalComponent/NaviBar";
import patientInfo from "@/components/workspace/patient/patientInfo";
import caseInfo from "@/components/workspace/patient/caseInfo";
import resultTable from "@/components/workspace/patient/resultTable";
// import Vue from 'vue'
// import VueRouter from 'vue-router'
//
// Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    },
    {
        path: '/navigator',
        name: 'navigator',
        component: NaviBar,
        redirect: '/dashhome',
        children: [
            {
                path: '/dashboard',
                name: 'dashboard',
                component: SideBar,
                redirect: 'dashHome',
                children: [
                    {
                        path: '/dashHome',
                        name: 'dashhome',
                        // component: patientInfo
                        component: caseInfo
                    },
                    {
                        path: '/dashHome2',
                        name: 'dashhome2',
                        component: patientInfo
                    },
                    {
                        path: "/dashHome3",
                        name: 'dashHome3',
                        component: resultTable
                    }
                ]
            }
        ]
    }
]

const router = createRouter({
                                history: createWebHashHistory(),
                                routes
                            })

export default router
