<template>
    <div style="width: 80%; border-radius: 20px; border-color: lightgray; border-style: solid; align-self: center">
        <p style="font-size: x-large; font-weight: bold">患者就诊信息</p>
        <el-form :model="form" label-width="120px" style="width: 80%; align-self: center; margin-top: 30px">
            <el-form-item label="就诊卡号">
                <el-input v-model="form.cardNo"/>
            </el-form-item>
            <el-form-item label="姓名">
                <el-input v-model="form.name"/>
            </el-form-item>
            <el-form-item label="性别">
                <el-select v-model="form.sex" placeholder="请选择患者性别">
                    <el-option label="男" value="1"/>
                    <el-option label="女" value="2"/>
                    <el-option label="未知" value="3"/>
                </el-select>
            </el-form-item>
            <el-form-item label="年龄">
                <el-input-number v-model="form.age"/>
                <el-select v-model="form.ageType" placeholder="请选择患者年龄类型">
                    <el-option label="岁" value="1"/>
                    <el-option label="月" value="2"/>
                    <el-option label="天" value="3"/>
                </el-select>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
export default {
    name: "patientInfo",
    data(){
        return {
            form: {
                cardNo: '',
                name: '',
                sex: '',
                age: 0,  // 1/12 for 1month, 1/365 for 1day
                ageType: '岁'
            }
        }
    }
}
</script>

<style scoped>

</style>