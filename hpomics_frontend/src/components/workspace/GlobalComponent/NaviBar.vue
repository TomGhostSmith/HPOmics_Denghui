<template>
    <el-menu
        :default-active='currentMenu'
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        style="min-width: 1300px">
        <el-menu-item :index="'/home'" @click="enterHome()">
            首页
        </el-menu-item>
        <!--    <el-menu-item :index="'/workTable'" @click="enterWorkTable()">-->
        <!--      导入缺陷-->
        <!--    </el-menu-item>-->
        <el-menu-item :index="'/dashBoard'" @click="enterDash()">
            控制面板
        </el-menu-item>
    </el-menu>
    <router-view @NavMenuClick="changeActive"/>
</template>

<script>
export default {
    name: "NaviBar"
}
</script>

<style scoped>
.el-menu {
    height: 60px;
}
</style>