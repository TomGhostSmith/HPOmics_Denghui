<template>
    <div style="border-radius: 20px; border-color: lightgray; border-style: solid; align-self: center; height: 350px;display: block;">
        <p style="font-size: x-large; font-weight: bold">基因组信息</p>
        <el-form :model="form" label-width="120px" style="width: 80%; margin-top: 30px; display: block;">
            <el-form-item label="患者测序结果">
                <el-upload
                    drag
                    accept=".vcf"
                    :action="$backend + '/uploadVCF'"
                    :auto-upload="false"
                    :on-success="onSuccessUpload"
                    style="align-self: center;width: 300px"
                    ref="uploader"
                    >
                    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                    <div class="el-upload__text">
                        将文件拖到此处，或<em>点击上传</em>
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
    emits: ['onUploaded'],
    data(){
        return{}
    },
    methods: {
        uploadFile()
        {
            this.$refs.uploader.submit()
        },
        onSuccessUpload(response, file, fileList)
        {
            let _this = this
            _this.$emit('onUploaded', file.name)
        }
    }

}
</script>

<style scoped>


</style>
