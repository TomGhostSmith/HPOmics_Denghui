<template>
    <div style="border-radius: 20px; border-color: lightgray; border-style: solid; align-self: center; height: 350px;display: block;">
        <p style="font-size: x-large; font-weight: bold">筛选设置
        </p>
<!--        <el-form-item label="预设方案">-->
        <span style="margin: 10px">预设方案</span>
            <el-select v-model="plan" placeholder="自定义" @change="loadPlan">
                <el-option v-for="(p,index) in plans" :label="p" :value="index" :key="index"/>
            </el-select>
<!--        </el-form-item>-->
        <el-form :model="form" label-width="120px" style="margin-top: 30px;">
            <el-row>
                <el-col :span="8">
                    <el-form-item label="预测目标">
                        <el-select v-model="form.taskType" placeholder="请选择预测目标">
                            <el-option label="疾病" :value="1"/>
                            <el-option label="基因" :value="2"/>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="信息含量计算">
                        <el-select v-model="form.icMethod" placeholder="请选择计算方法">
                            <el-option label="根据疾病计算" :value="1"/>
                            <el-option label="根据基因计算" :value="2"/>
                            <el-option label="综合计算" :value="3"/>
                            <el-option label="根据数据集计算" :value="4"/>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="相似度计算">
                        <el-select v-model="form.similarity" placeholder="请选择计算方法">
                            <el-option label="根据Lin方法计算" :value="1"/>
                            <el-option label="根据J-C方法计算" :value="2"/>
                            <el-option label="根据IC方法计算" :value="3"/>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="增加HPO节点">
                        <el-select v-model="form.useAncestor" placeholder="请选择计算方法">
                            <el-option label="不增加" :value="1"/>
                            <el-option label="为预测目标增加" :value="2"/>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="蛋白互作信息">
                        <el-select v-model="form.usePPI" placeholder="请选择是否使用">
                            <el-option label="使用" :value="true"/>
                            <el-option label="不使用" :value="false"/>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="基因自身权重">
                        <el-input-number :precision="2" :step="0.1" :max="1" :min="0" :disabled="form.usePPI == false" v-model="form.ppiSelfProportion" placeholder="请输入比例" style="width: 200px"/>

                    </el-form-item>

                    <el-form-item label="基因家族权重">
                        <el-input-number :precision="2" :step="0.1" :max="1" :min="0" :disabled="form.usePPI == false" v-model="form.ppiDirectProportion" placeholder="请输入比例" style="width: 200px"/>

                    </el-form-item>

                    <el-form-item label="互作基因权重">
                        <el-input-number :precision="2" :step="0.1" :max="1" :min="0" :disabled="form.usePPI == false" v-model="form.ppiIndirectProportion" placeholder="请输入比例" style="width: 200px"/>

                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="疾病基因互转">
                        <el-select v-model="form.convertProportionMethod" placeholder="请选择计算方法">
                            <el-option label="不使用" :value="1"/>
                            <el-option label="固定比例" :value="2"/>
                            <el-option label="浮动比例" :value="3"/>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="互转最大比例">
                        <el-input-number :precision="2" :step="0.1" :max="1" :min="0" :disabled="form.convertProportionMethod == 1" v-model="form.convertMaxProportion" placeholder="请输入比例" style="width: 200px"/>
                    </el-form-item>

                    <el-form-item label="使用CADD">
                        <el-select v-model="form.caddMethod" placeholder="请选择计算方法">
                            <el-option label="不使用" :value="1"/>
                            <el-option label="固定比例" :value="2"/>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="CADD比例">
                        <el-input-number :precision="2" :step="0.1" :max="1" :min="0" :disabled="form.caddMethod == 1" v-model="form.caddMaxProportion" placeholder="请输入比例" style="width: 200px"/>
                    </el-form-item>
                </el-col>
            </el-row>

        </el-form>
    </div>
</template>

<script>
export default {
    name: "taskSetting",
    data(){
        return {
            plan: '',
            form: {
                taskType: null,
                icMethod: null,
                similarity: null,
                useAncestor: null,
                convertProportionMethod: null,
                convertMaxProportion: null,
                usePPI: null,
                ppiSelfProportion: null,
                ppiDirectProportion: null,
                ppiIndirectProportion: null,
                caddMethod: null,
                caddMaxProportion: null
            },
            plans: ['疾病预测', '致病基因预测']
        }
    },
    methods: {
        getSetting()
        {
            let _this = this
            let selfP = _this.form.ppiSelfProportion
            let directP = _this.form.ppiDirectProportion
            let indirectP = _this.form.ppiIndirectProportion
            let sumEQOne = (selfP + directP + indirectP === 1)
            let basicFinished = _this.form.taskType != null && _this.form.icMethod != null && _this.form.similarity != null && _this.form.useAncestor != null
            let PPIFinished = _this.form.usePPI != null
            let convertFinished = _this.form.convertProportionMethod != null
            let CADDFinished = _this.form.caddMethod != null
            let allFinished = basicFinished && PPIFinished && convertFinished && CADDFinished

            if (!allFinished)
            {
                _this.$message.error('请填写完整筛选设置')
                return null
            }
            if (_this.form.usePPI && !sumEQOne)
            {
                _this.$message.error('PPI 权重有误，请确保权重之和为1')
                return null
            }
            if (_this.form.convertProportionMethod != 1 && _this.form.convertMaxProportion == null)
            {
                _this.$message.error('互转权重有误')
                return null
            }
            if (_this.form.CADDMethod != 1 && _this.form.caddMaxProportion == null)
            {
                _this.$message.error('CADD权重有误')
                return null
            }
            return _this.form
        },
        loadDefaultPlanList()
        {

        },
        loadPlan()
        {
            if (this.plan == 0)
            {
                this.form = {
                    taskType: 1,
                    icMethod: 3,
                    similarity: 3,
                    useAncestor: 1,
                    convertProportionMethod: 2,
                    convertMaxProportion: 0.6,
                    usePPI: false,
                    ppiSelfProportion: 1,
                    ppiDirectProportion: 0,
                    ppiIndirectProportion: 0,
                    caddMethod: 2,
                    caddMaxProportion: 1
                }
            }
            else if (this.plan == 1)
            {
                this.form = {
                    taskType: 2,
                    icMethod: 3,
                    similarity: 3,
                    useAncestor: 2,
                    convertProportionMethod: 3,
                    convertMaxProportion: 1,
                    usePPI: true,
                    ppiSelfProportion: 0.2,
                    ppiDirectProportion: 0.3,
                    ppiIndirectProportion: 0.5,
                    caddMethod: 1,
                    caddMaxProportion: 0
                }
            }
        }
    }
}
</script>

<style scoped>

</style>
