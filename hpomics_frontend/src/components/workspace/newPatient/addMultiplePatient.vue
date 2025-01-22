<template>
    <div style="height: 20px"/>
    <div style="display: block; vertical-align: center;width: 90%; align-self: center">
        <div style="display: inline-block; width: calc(50% - 10px); margin-right: 10px; vertical-align: top;">
            <multiple-patient-info ref="HPOUploader" @onUploaded="onUploadHPO"/>
        </div>
        <div style="display: inline-block; width: calc(50% - 10px); margin-left: 10px; vertical-align: top;">
            <multiple-case-info ref="VCFUploader" @onUploaded="onUploadVCF"/>
        </div>
    </div>
    <div style="width: 90%; align-self: center; margin-top: 20px">
        <task-setting ref="taskSetting"/>
    </div>
    <el-button style="width: 150px;height: 100px;margin-top: 20px; align-self: center" type="primary" @click="submit">批量添加患者</el-button>
</template>

<script>
import MultiplePatientInfo from "@/components/workspace/GlobalComponent/multiplePatientInfo";
import MultipleCaseInfo from "@/components/workspace/GlobalComponent/multipleCaseInfo";
import TaskSetting from "@/components/workspace/GlobalComponent/taskSetting";
export default {
    name: "addMultiplePatient",
    components: {TaskSetting, MultipleCaseInfo, MultiplePatientInfo},
    data()
    {
        return {
            hpoFileList: null,
            vcfFileList: null,
            settings: null
        }
    },
    methods: {
        submit()
        {
            let _this = this
            _this.settings = _this.$refs.taskSetting.getSetting()
            if (_this.settings != null)
            {
                _this.$refs.HPOUploader.uploadFiles()
                if (_this.settings.caddMethod == 1)
                {
                    _this.vcfFileList = []
                }
                else
                {
                    _this.$refs.VCFUploader.uploadFiles()
                }
            }
        },
        onUploadHPO(fileList)
        {
            this.hpoFileList = fileList
            this.tryStartProcess()
        },
        onUploadVCF(fileList)
        {
            this.vcfFileList = fileList
            this.tryStartProcess()
        },
        tryStartProcess()
        {
            let _this = this
            if (_this.hpoFileList != null && _this.vcfFileList != null)
            {
                let _this = this
                _this.$axios.post(_this.$backend + "/addMultiplePatientTask", {
                    patientFileNames: _this.hpoFileList,
                    vcfFileNames: _this.vcfFileList,
                    setting: _this.settings
                }).then(resp => {
                    if (resp.status === 200)
                    {
                        _this.$message.success('提交成功！')
                        _this.$router.push("/jobList")
                    }
                })
            }
        }
    }
}
</script>

<style scoped>

</style>
