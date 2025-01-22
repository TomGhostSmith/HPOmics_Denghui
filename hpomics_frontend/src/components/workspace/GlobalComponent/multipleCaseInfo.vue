<template>
    <div
        v-loading="uploading"
        element-loading-text="上传中..."
        style="border-radius: 20px; border-color: lightgray; border-style: solid; align-self: center; height: 350px;display: block;">
        <p style="font-size: x-large; font-weight: bold">基因组信息</p>
        <el-form :model="form" label-width="120px" style="width: 80%; margin-top: 30px; display: block;">
            <el-form-item label="患者测序结果">
                <el-upload
                    drag
                    accept=".vcf"
                    multiple
                    :action="$backend + '/uploadVCF'"
                    style="align-self: center;width: 300px"
                    :auto-upload="false"
                    :on-success="onSuccessUpload"
                    ref="uploader"
                >
                    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                    <div class="el-upload__text">
                        将文件拖到此处，或<em>点击上传</em>
                    </div>
                </el-upload>
            </el-form-item>

        </el-form>
        <el-progress v-show="uploading" :percentage="percentage" stroke-width="20"  style="position: fixed; z-index: 3000; width: 80%; margin-left: 10%;bottom: 50px; position: absolute"/>

    </div>
</template>

<script>
export default {
    name: "multipleCaseInfo",
    emits: ['onUploaded'],
    data()
    {
        return {
            fileList: [],
            totalCount: 0,
            uploading: false,
            percentage: 0,
            intervalID: null
        }
    },
    methods: {
        uploadFiles()
        {
            let _this = this
            _this.fileList = []
            _this.uploading = true
            _this.$refs.uploader.submit()
            _this.intervalID = setInterval(function(){
                if (_this.totalCount != 0)
                {
                    _this.percentage = (_this.fileList.length / _this.totalCount * 100).toFixed(2)
                }
            }, 100)
        },
        onSuccessUpload(response, file, fileList)
        {
            let _this = this
            _this.fileList.push(file.name)
            _this.totalCount = fileList.length

            if (_this.fileList.length == fileList.length)  // all are uploaded
            {
                _this.$emit('onUploaded', _this.fileList)
                _this.uploading = false
                if (_this.intervalID != null)
                {
                    clearInterval(_this.intervalID)
                }
            }
        }
    }
}
</script>

<style scoped>
::v-deep .el-upload-dragger{
    padding-top: 0;
    padding-bottom: 0;
}

::v-deep .el-upload-list {
    max-height: 120px; /* Set max height for the file list */
    overflow-y: auto; /* Enable vertical scrolling */
}

::v-deep .el-loading-mask {
    border-radius: 20px;
}
</style>
