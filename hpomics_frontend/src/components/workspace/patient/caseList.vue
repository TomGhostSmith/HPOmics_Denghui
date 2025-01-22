<template>
    <el-button type="plain" style="width: 100px; min-height: 50px;margin-left: 20px; margin-top: 30px" @click="back">返回</el-button>
    <p style="font-size: x-large; font-weight: bold; margin-bottom: 10px; margin-top: 0">病例列表</p>
    <el-table :data="tableData" style="max-width: 80%; align-self: center">
        <el-table-column label="患者身份" align="center" sortable>
            <template #default="scope">
                <p style="margin: 0px">{{ scope.row.patientIdentity }}</p>
            </template>
        </el-table-column>
        <el-table-column label="当前状态" align="center" sortable>
<!--            <template #default="scope">-->
<!--                <el-progress :percentage="scope.row.status*50" :status="scope.row.status == 2? 'success' : ''" :stroke-width="26"/>-->
<!--            </template>-->
            <template #default="scope">
                <div style="margin: 0px" v-html="statuses[scope.row.status]" />
            </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
            <template #default="scope">
                <el-button :disabled="scope.row.status != 2" @click="openCaseList(scope.row.patientIdentity)">查看结果</el-button>
                <!--                <p v-for="(item, index) in scope.row.progress" :key="index" style="margin: 0px">{{ item }}</p>-->
            </template>
        </el-table-column>
    </el-table>
</template>

<script>
export default {
    name: "caseList",
    data(){
        return {
            tableData: [],
            taskName: '',
            intervalID: null,
            statuses: ['<span style="color: red">等待中</span>', '<span style="color: orange">正在处理</span>', '<span style="color: #32d232">已处理</span>']
        }
    },
    mounted()
    {
        let _this = this
        _this.taskName = this.$route.params.taskName
        _this.loadData()
        _this.intervalID = setInterval(function(){
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
            _this.$axios.get(_this.$backend + "/getTaskProgress/" + _this.taskName)
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
        openCaseList(patientIdentity)
        {
            let _this = this
            _this.$router.push(
                {
                    name: 'caseResult',
                    params: {
                        taskName: _this.taskName,
                        patientIdentity: patientIdentity
                    }
                })
        },
        back()
        {
            this.$router.push('/jobList')
        }
    }
}
</script>

<style scoped>

</style>
