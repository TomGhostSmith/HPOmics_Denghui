<template>
    <router-view/>
</template>

<script>

export default {
  name: 'App',
    mounted()
    {
        window.addEventListener('hashchange',()=>{
            var currentPath = window.location.hash.slice(1); // 获取输入的路由
            console.log(currentPath);
            console.log(this.$router.path);
            if(this.$router.path !== currentPath){
                this.$router.push(currentPath); // 动态跳转
            }
        },false);
    }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
    height: 100%;
}

html, body
{
    margin: 0;
    height: 100%;
}
</style>
