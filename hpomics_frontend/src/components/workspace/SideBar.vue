<template>
    <el-container style="height: calc(100% - 60px); border: 1px solid #eee">
        <el-aside width="205px" style="background-color: rgb(238, 241, 246)">
<!--            <el-menu default-active="2" class="=el-menu-vertical-demo" style="margin-top: 5px;">-->
<!--                <el-sub-menu index="1">-->
<!--                    <template #title>-->
<!--                        <Menu size="30"></Menu>-->
<!--                        <span>Title</span>-->
<!--                    </template>-->
<!--                    <el-menu-item index="1-1">a</el-menu-item>-->
<!--                </el-sub-menu>-->
<!--            </el-menu>-->



            <el-menu :default-active="active" class="el-menu-vertical-demo" style="margin-top: 5px;">
                <router-link to="/dashHome">
                    <el-menu-item index="2">
                        <ElIcon :size="30">
<!--                            <edit  style="color: black"/>-->
                            <Menu/>
                        </ElIcon>
<!--                        <span slot="title">Welcome</span>-->
<!--                        <span>Welcome</span>-->
                        <template #title><span>Welcome</span></template>
                    </el-menu-item>
                </router-link>
                <el-sub-menu index="1">
<!--                    <template v-slot:title>-->
<!--                        <i class="el-icon-document"></i>-->
<!--                        <span slot="title">缺陷追溯</span>-->
                        <template #title><span>患者信息管理</span></template>
<!--                        <slot name="title">缺陷追溯</slot>-->
<!--                    </template>-->
<!--                    <template v-slot:title>1</template>-->
                    <router-link to="/addSinglePatient">
                        <el-menu-item index="1-1">录入单病例</el-menu-item>
                    </router-link>
                    <router-link to="/addMultiplePatient">
                        <el-menu-item index="1-2">批量导入病例</el-menu-item>
                    </router-link>
                    <router-link to="/jobList">
                        <el-menu-item index="1-3">病例列表</el-menu-item>
                    </router-link>
                </el-sub-menu>

                <el-sub-menu index="2">
                    <template v-slot:title>
                        <i class="el-icon-user-solid"></i>
<!--                        <span slot="title">开发统计</span>-->
                        <span>系统</span>
                    </template>
                    <router-link to="/">
                        <el-menu-item index="2-1">设置</el-menu-item>
                    </router-link>
                </el-sub-menu>
            </el-menu>
        </el-aside>

        <el-container>
            <router-view @listClick="decideActive"></router-view>
            <el-footer></el-footer>
        </el-container>
    </el-container>
</template>

<script>
export default {
    name: "SideBar",
    data(){
        return {
            active: ''
        }
    },
    mounted()
    {

    },
    created()
    {

    },
    methods: {

    }
}
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 500px;
    text-align: left;
}
.el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
}

.el-menu a
{
    text-decoration-line: none;
}

.el-aside {
    color: #333;
}
</style>
