<template>
    <div style="height: 20px"/>
    <div style="display: block; vertical-align: center;width: 90%; align-self: center">
        <div style="display: inline-block; width: calc(50% - 10px); margin-right: 10px; vertical-align: top;">
            <patient-info ref="patientInfo"/>
        </div>
        <div style="display: inline-block; width: calc(50% - 10px); margin-left: 10px; vertical-align: top;">
            <case-info ref="caseInfo" @onUploaded="onVCFUploaded"/>
        </div>
    </div>
    <div style="width: 90%; align-self: center; margin-top: 20px">
        <task-setting ref="taskSetting"/>
    </div>
    <el-button style="width: 150px;height: 100px;margin-top: 20px; align-self: center" type="primary" @click="submit">添加患者</el-button>
</template>

<script>
import PatientInfo from "@/components/workspace/GlobalComponent/patientInfo";
import CaseInfo from "@/components/workspace/GlobalComponent/caseInfo";
import TaskSetting from "@/components/workspace/GlobalComponent/taskSetting";
export default {
    name: "addNewSinglePatient",
    components: {TaskSetting, CaseInfo, PatientInfo},
    data()
    {
        return {
            form: {
                settings: null,
                patient: null
            }
        }
    },
    methods: {
        submit()
        {
            let _this = this
            _this.form.settings = _this.$refs.taskSetting.getSetting()
            _this.form.patient = _this.$refs.patientInfo.getPatientInfo()
            if (_this.form.settings != null && _this.form.patient != null)
            {
                _this.$refs.caseInfo.uploadFile()
            }
        },
        onVCFUploaded(fileName)
        {
            let _this = this
            _this.form.patient.vcfFileName = fileName
            _this.$axios.post(_this.$backend + "/addSinglePatientTask", {
                patient: _this.form.patient,
                setting: _this.form.settings
            }).then(resp => {
                if (resp.status === 200)
                {
                    _this.$message.success('提交成功！')
                }
            })

        }
    }
}
</script>

<style scoped>

</style>
