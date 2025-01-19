<template>
    <div class="page-view">
        <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="form" :rules="rules">
            <a-row :gutter="24">
                <a-col span="24">
                    <a-form-item label="任务名称" name="title">
                        <a-input placeholder="请输入任务名称" v-model:value="form.title"></a-input>
                    </a-form-item>
                </a-col>
            </a-row>

            <a-row :gutter="24">
                <a-col span="24">
                    <a-form-item label="任务描述" name="description">
                        <a-input placeholder="请输入任务描述" v-model:value="form.description"></a-input>
                    </a-form-item>
                </a-col>
            </a-row>

            <a-row :gutter="24">
                <a-col span="24">
                    <a-form-item label="选择算法" name="algorithm">
                        <a-select placeholder="请选择算法" v-model:value="form.algorithm">
                            <a-select-option v-for="item in modal.AlgorithmData" :key="item.id" :value="item.id">
                                {{ item.title }}
                            </a-select-option>
                        </a-select>
                    </a-form-item>
                </a-col>
            </a-row>

            <a-row :gutter="24">
                <a-col span="24">
                    <a-form-item label="选择数据" name="data">
                        <a-select placeholder="请选择数据" v-model:value="form.data">
                            <a-select-option v-for="item in modal.ROSData" :key="item.id" :value="item.id">
                                {{ item.name }}
                            </a-select-option>
                        </a-select>
                    </a-form-item>
                </a-col>
            </a-row>


            <a-row :gutter="24">
                <a-col span="12">
                    <a-form-item label="评测开始" name="evaluate_start_time">
                        <a-input-number v-model:value="form.evaluate_start_time" :min="0" :max="30" placeholder="请输入.." />
                    </a-form-item>
                </a-col>
                <a-col span="12">
                    <a-form-item label="评测结束" name="evaluate_start_time">
                        <a-input-number v-model:value="form.evaluate_end_time" :min="0" :max="30" placeholder="请输入.." />
                    </a-form-item>
                </a-col>
            </a-row>

            <a-col span="24">
                <a-button type="primary" @click="handleOk">确认</a-button>
                <a-button style="margin-left: 8px" @click="resetForm">重置</a-button>
            </a-col>
        </a-form>
    </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { FormInstance, message } from 'ant-design-vue';
import { createApi } from '/@/api/admin/task';
import { listApi as listAlgorithmApi } from '/@/api/admin/algorithm'
import { listApi as listDataApi } from '/@/api/admin/data'
const router = useRouter();

const form = reactive({
    id: undefined,
    title: undefined,
    description: undefined,
    status: undefined,
    evaluate_result: undefined,
    algorithm: undefined,
    data: undefined,
    evaluate_start_time: undefined,
    evaluate_end_time: undefined,
});

const rules = {
    title: [{ required: true, message: '请输入', trigger: 'change' }],
    description: [{ required: true, message: '请输入', trigger: 'change' }],
    algorithm: [{ required: true, message: '请输入', trigger: 'change' }],
    data: [{ required: true, message: '请输入', trigger: 'change' }],
};

const modal = reactive({
    AlgorithmData: [],
    ROSData: [],
});

onMounted(() => {
    getAlgorithmList();
    getDataList();
});

const getAlgorithmList = () => {
    listAlgorithmApi({}).then(res => {
        modal.AlgorithmData = res.data
        console.log(modal.AlgorithmData)
    })
}

const getDataList = () => {
    listDataApi({}).then(res => {
        res.data.forEach((item, index) => {
            item.index = index + 1
        })
        modal.ROSData = res.data
    })
}

const myform = ref<FormInstance>();

const submitSuccess = () => {
    router.push({ name: 'my_task' })
    message.success('提交成功！')
}
const handleOk = async () => {
    try {
        await myform.value?.validate();
        try {
            
            const res = await createApi(form);
            submitSuccess();
            resetForm();
        } catch (err) {
            console.log(err);
            message.error(err.message || '操作失败');
        }
    } catch (err) {
        console.log('表单验证失败');
    }
};

const resetForm = () => {
    for (const key in form) {
        form[key] = undefined;
    }
    myform.value?.resetFields();
};

</script>

<style scoped lang="less">
.page-view {
    min-height: 100%;
    background: #fff;
    padding: 24px;
    display: flex;
    flex-direction: column;
}
</style>
