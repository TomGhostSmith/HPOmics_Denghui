<template>
    <p style="font-size: x-large; font-weight: bold; margin-bottom: 30px">任务列表</p>
    <el-table :data="tableData" style="max-width: 80%; align-self: center">
        <el-table-column label="上传时间" align="center">
            <template #default="scope">
                <p style="margin: 0px">{{ scope.row.submitTime }}</p>
            </template>
        </el-table-column>
        <el-table-column label="病例数量" align="center">
            <template #default="scope">
                <p style="margin: 0px">{{ scope.row.taskCount }}</p>
            </template>
        </el-table-column>
        <el-table-column prop="excess" label="处理进度" align="left">
            <template #default="scope">
                <el-progress :percentage="scope.row.progress" :status="scope.row.progress == 100? 'success' : ''" :stroke-width="26"/>
            </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
            <template #default="scope">
                <el-button @click="openCaseList(scope.row.taskName)">查看结果</el-button>
<!--                <p v-for="(item, index) in scope.row.progress" :key="index" style="margin: 0px">{{ item }}</p>-->
            </template>
        </el-table-column>
    </el-table>
</template>

<script>
export default {
    name: "jobList",
    data()
    {
        return {
            tableData: [
                {
                    submitTime: 'time',
                    taskCount: 10,
                    progress: 90,
                    taskName: 'ttaasskk'
                }
            ],
            intervalID: null
        }
    },
    mounted()
    {
        let _this = this
        _this.loadData()
        _this.intervalID = setInterval(function ()
        {
            _this.loadData()
        }, 500)
    },
    beforeRouteLeave(to, from, next)
    {
        clearInterval(this.intervalID)
        next()
    },
    methods: {
        loadData()
        {
            let _this = this
            _this.$axios.get(_this.$backend + "/getAllProgress")
                .then(resp => {
                    if (resp.status === 200)
                    {
                        _this.tableData = resp.data
                    }
                }).catch(err => {
                if (_this.intervalID != null)
                {
                    clearInterval(_this.intervalID)
                }
            })
        },
        openCaseList(taskName)
        {
            this.$router.push({name: 'caseList', params: {taskName: taskName}})
        }
    }
}
</script>

<style scoped>

</style>
