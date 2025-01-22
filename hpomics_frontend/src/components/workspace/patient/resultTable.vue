<template>
    <el-button type="plain" style="width: 100px; min-height: 50px;margin-left: 20px; margin-top: 30px" @click="back">返回</el-button>
    <p style="font-size: x-large; font-weight: bold; margin-bottom: 10px; margin-top: 0">预测结果</p>
    <el-table :data="tableData" style="max-width: 80%; align-self: center" v-loading="isLoading">
        <el-table-column label="疾病" width="250" fixed align="center">
            <template #default="scope">
                <p>{{ scope.row.diseaseID }}</p>
                <p>{{ scope.row.diseaseName }}</p>
            </template>
        </el-table-column>
<!--        next three column only shows number, e.g. overlap: 5 excess: 10, loss: 8-->
        <el-table-column label="相似症状" align="left" width="300">
            <template #default="scope">
                <p v-for="(item, index) in scope.row.overlap" :key="index" style="margin: 0px">{{ item }}</p>
            </template>
        </el-table-column>
        <el-table-column prop="excess" label="无关症状" align="left" width="300">
            <template #default="scope">

            <p v-for="(item, index) in scope.row.excess" :key="index" style="margin: 0px">{{ item }}</p>
            </template>
        </el-table-column>
        <el-table-column prop="loss" label="未表现症状" align="left" width="300">
            <template #default="scope">

            <p v-for="(item, index) in scope.row.loss" :key="index" style="margin: 0px">{{ item }}</p>
            </template>
        </el-table-column>
        <el-table-column label="患病风险" fixed="right" min-width="280" align="center">
            <template #default="scope">
                <el-progress :percentage="scope.row.possibility" :color="calcColor" :stroke-width="26"/>
            </template>
        </el-table-column>


    </el-table>
<!--    <el-input-number v-model="tableData[0].possibility"/>-->
</template>

<script>
import translation from '../../../assets/translation.json'
// import res from '../../../assets/exampleResult.json'
export default {
    name: "resultTable",
    data(){
        return {
            tableData: [],
            taskName: null,
            patientIdentity: null,
            isLoading: false
        }
    },
    mounted()
    {
        this.taskName = this.$route.params.taskName
        this.patientIdentity = this.$route.params.patientIdentity
        this.loadResult()
    },
    methods: {
        calcColor(percentage)
        {
            percentage = percentage/100
            var midPoint = 50
            var red = Math.min(255 * percentage * (100/midPoint), 235);
            var green = Math.min(255 * (1 - percentage)*(100/(100-midPoint)), 235);
            var blue = 0;

            if (red + green > 350)
            {
                red = red/(red + green) * 380
                green = green/(red + green) * 380
            }

            console.log("red = " + red + ", green = " + green)
            var color = "#" + Math.round(red).toString(16).padStart(2, '0')
                + Math.round(green).toString(16).padStart(2, '0')
                + blue.toString(16).padStart(2, '0')
            console.log(color)
            return color
        },
        loadResult()
        {
            // use axios to get result
            let _this = this
            _this.isLoading = true
            _this.$axios.get(_this.$backend + '/getResult/' + _this.taskName + '/' + _this.patientIdentity).then(resp => {
                if (resp.status === 200)
                {
                    for (let item of resp.data)
                    {
                        if (parseInt(item.possibility) < 30)
                        {
                            break
                        }
                        let disease = {
                            diseaseID: item.diseaseID,
                            diseaseName: item.diseaseName,
                            overlap: [],
                            excess: [],
                            loss: [],
                            possibility: item.possibility
                            // possibility: (item['possibility'] * 100).toFixed(2)
                        }
                        for (let term of item.overlapHPO)
                        {
                            if (disease.overlap.length >= 5)
                            {
                                disease.overlap.push("(" + (item.overlapHPO.length - 5) + " more)")
                                break
                            }
                            disease.overlap.push(this.getTranslation(term))
                        }
                        for (let term of item.excessHPO)
                        {
                            if (disease.excess.length >= 5)
                            {
                                disease.excess.push("(" + (item.excessHPO.length - 5) + " more)")
                                break
                            }
                            disease.excess.push(_this.getTranslation(term))
                        }
                        for (let term of item.lossHPO)
                        {
                            if (disease.loss.length >= 5)
                            {
                                disease.loss.push("(" + (item.lossHPO.length - 5) + " more)")
                                break
                            }
                            disease.loss.push(_this.getTranslation(term))
                        }
                        _this.tableData.push(disease)
                        _this.isLoading = false

                    }
                }
            })
        },
        getTranslation(term)
        {
            // return term
            let obj = translation[term]
            if (obj)
            {
                return term + ": " + obj['Chinese']
            }
            else
            {
                return term
            }
        },
        back()
        {
            let _this = this
            _this.$router.push('/caseList/' + _this.taskName)
        }
    }
}
</script>

<style scoped>

</style>
