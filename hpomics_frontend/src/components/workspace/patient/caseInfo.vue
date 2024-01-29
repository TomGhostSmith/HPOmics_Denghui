<template>
        <div style="width: 80%; border-radius: 20px; border-color: lightgray; border-style: solid; align-self: center">
            <p style="font-size: x-large; font-weight: bold">患者疾病信息</p>
            <el-form :model="form" label-width="120px" style="width: 80%; align-self: center; margin-top: 30px">
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
                <el-form-item label="患者测序结果">

                    <el-upload
                        drag
                        style="align-self: center"
                    >
                        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                        <div class="el-upload__text">
                            Drop file here or <em>click to upload</em>
                        </div>
                    </el-upload>
                </el-form-item>

            </el-form>
        </div>
</template>

<script>
import translation from '../../../assets/translation.json'
import {ref} from "vue";
export default {
    // this component is used for record patient sequence and HPO
    name: "caseInfo",
    data(){
        return{
            form:{
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
        }
    }
}
</script>

<style scoped>

</style>