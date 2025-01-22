<template>
    <div style="border-radius: 20px; border-color: lightgray; border-style: solid; align-self: center; height: 350px;display: block;">
        <p style="font-size: x-large; font-weight: bold; margin-bottom: 15px">患者临床信息</p>
        <el-form :model="form" label-width="120px" style="width: 80%; margin-top: 15px;">
            <el-form-item label="就诊卡号">
                <el-input v-model="form.identity"/>
            </el-form-item>
<!--            <el-form-item label="姓名">-->
<!--                <el-input v-model="form.name"/>-->
<!--            </el-form-item>-->
            <el-form-item label="性别">
                <el-select v-model="form.gender" placeholder="请选择患者性别">
                    <el-option label="男" :value="1"/>
                    <el-option label="女" :value="2"/>
                    <el-option label="未知" :value="3"/>
                </el-select>
            </el-form-item>
            <el-form-item label="年龄">
                <div style="display: block; width: 100%;text-align: start">
                    <el-input-number :max="120" :min="0" v-model="form.ageYear" style="width: 150px; display: inline-block; margin-right: 20px;"/><p style="display: inline-block; margin: 2px 0">年</p>
                </div>
                <div style="display: block; width: 100%;text-align: start">
                    <el-input-number :max="11" :min="0" v-model="form.ageMonth" style="width: 150px; display: inline-block; margin-right: 20px"/><p style="display:inline-block; margin: 2px 0">月</p>
                </div>
                <div style="display: block; width: 100%;text-align: start">
                    <el-input-number :max="29" :min="0" v-model="form.ageDay" style="width: 150px; display: inline-block; margin-right: 20px"/><p style="display: inline-block; margin: 2px 0">天</p>
                </div>
                <br>
            </el-form-item>
<!--            <p>可用Y/M/D表示年/月/日</p>-->
<!--            <p>例如1Y6M3D表示1岁6个月3天</p>-->
            <el-form-item label="患者症状">
                <el-select-v2
                    style="width:600px;"
                    v-model="form.HPO"
                    multiple
                    filterable
                    remote
                    :remote-method="filterHPO"
                    clearable
                    :options="HPOoptions"
                    :loading="HPOloading"
                    placeholder="请选择患者症状"/>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import {ref} from "vue";
import translation from "@/assets/translation.json";

export default {
    name: "patientInfo",
    data(){
        return {
            form: {
                identity: null,
                gender: null,
                ageYear: 0,
                ageMonth: 0,
                ageDay: 0,
                ageType: '岁',
                HPO: []
            },
            HPOoptions: [],
            HPOloading: ref(false),
            HPOlist: []
        }
    },
    mounted()
    {
        // console.log(translation["HP:0000001"])
        // console.log(translation["HP:0000002"])
        // console.log(translation["HP:0000003"])
        // console.log(this.HPOlist)
        for (var [key, value] of Object.entries(translation))
        {
            this.HPOlist.push({value: `${key}`, label: `${key} ${value['Chinese']}`, pinyin: value["pinyin"]})
        }
    },
    methods: {
        filterHPO(str)
        {
            this.HPOloading = true
            this.HPOoptions = this.HPOlist.filter((item) => {
                return item.pinyin.startsWith(str.toLowerCase())
            })
            this.HPOloading = false
            console.log(this.form.HPO)
        },
        getPatientInfo()
        {
            let _this = this
            let finished = _this.form.identity != null && _this.form.HPO.length > 0
            if (!finished)
            {
                _this.$message.error('请填写完整患者相关信息')
                return null
            }
            return {
                identity: _this.form.identity,
                name: _this.form.name,
                gender: _this.form.gender,
                age: _this.form.ageYear * 365 + _this.form.ageMonth * 30 + _this.form.ageDay,
                hpoList: _this.form.HPO,
                vcfFileName: ''
            }
        }
    }
}
</script>

<style scoped>

</style>
