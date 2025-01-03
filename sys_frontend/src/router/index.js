import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            component: resolve => require(['../login.vue'], resolve)
        },
        {
            path: '/login',
            component: resolve => require(['../login.vue'], resolve)
        },
        {
            path: '/admin',
            component: resolve => require(['../admin/common/Home.vue'], resolve),
            children:[
                {
                    path: '/account_admin',
                    component: resolve => require(['../admin/page/account_admin.vue'], resolve)
                },
                {
                    path: '/course',
                    component: resolve => require(['../admin/page/course.vue'], resolve)
                },
                {
                    path: '/sc_system',
                    component: resolve => require(['../admin/page/sc_system.vue'], resolve)
                }
            ]
        }
    ]
})
