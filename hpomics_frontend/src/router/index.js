import {createRouter, createWebHashHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SideBar from "@/components/workspace/SideBar.vue";
import NaviBar from "@/components/workspace/NaviBar";
import patientInfo from "@/components/workspace/GlobalComponent/patientInfo";
import caseInfo from "@/components/workspace/GlobalComponent/caseInfo";
import resultTable from "@/components/workspace/patient/resultTable";
import addSinglePatient from "@/components/workspace/newPatient/addSinglePatient";
import addMultiplePatient from "@/components/workspace/newPatient/addMultiplePatient";
import jobList from "@/components/workspace/patient/jobList";
import caseList from "@/components/workspace/patient/caseList";
// import Vue from 'vue'
// import VueRouter from 'vue-router'
//
// Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView,
        redirect: '/jobList'
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
                redirect: '/jobList',
                children: [
                    {
                        path: '/addSinglePatient',
                        name: 'addSinglePatient',
                        component: addSinglePatient
                    },
                    {
                        path: '/addMultiplePatient',
                        name: 'addMultiplePatient',
                        component: addMultiplePatient
                    },
                    {
                        path: '/jobList',
                        name: 'jobList',
                        component: jobList
                    },
                    {
                        path: '/caseList/:taskName',
                        name: 'caseList',
                        component: caseList
                    },
                    {
                        path: '/caseResult/:taskName/:patientIdentity',
                        name: 'caseResult',
                        component: resultTable
                    },
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
