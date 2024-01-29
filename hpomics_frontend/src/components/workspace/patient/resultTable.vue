<template>
    <el-table :data="tableData" style="max-width: 80%; align-self: center">
        <el-table-column prop="disease" label="疾病" width="250" fixed align="center"/>
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
        <el-table-column label="患病风险" fixed="right" min-width="180" align="center">
            <template #default="scope">
                <el-progress :percentage="scope.row.possibility" :color="calcColor" :text-inside="true" :stroke-width="26"/>
            </template>
        </el-table-column>


    </el-table>
<!--    <el-input-number v-model="tableData[0].possibility"/>-->
</template>

<script>
import translation from '../../../assets/translation.json'
import res from '../../../assets/exampleResult.json'
export default {
    name: "resultTable",
    data(){
        return {
            tableData: []
        }
    },
    mounted()
    {
        this.loadResult()
    },
    methods: {
        calcColor(percentage)
        {
            percentage = percentage/100
            var midPoint = 80
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
            for (let item of res)
            {
                console.log(item)
                let disease = {
                    disease: item['disease'],
                    overlap: [],
                    excess: [],
                    loss: [],
                    // possibility: Math.round(item['possibility'] * 100)
                    possibility: (item['possibility'] * 100).toFixed(2)
                }
                for (let term of item['overlap'])
                {
                    if (disease.overlap.length >= 5)
                    {
                        disease.overlap.push("(" + (item['overlap'].length - 5) + " more)")
                        break
                    }
                    disease.overlap.push(this.getTranslation(term))
                }
                for (let term of item['excess'])
                {
                    if (disease.excess.length >= 5)
                    {
                        disease.excess.push("(" + (item['excess'].length - 5) + " more)")
                        break
                    }
                    disease.excess.push(this.getTranslation(term))
                }
                for (let term of item['loss'])
                {
                    if (disease.loss.length >= 5)
                    {
                        disease.loss.push("(" + (item['loss'].length - 5) + " more)")
                        break
                    }
                    disease.loss.push(this.getTranslation(term))
                }
                this.tableData.push(disease)
            }
        },
        getTranslation(term)
        {
            let obj = translation[term]
            if (obj)
            {
                return term + ": " + obj['Chinese']
            }
            else
            {
                return term
            }
        }
    }
}
</script>

<style scoped>

</style>