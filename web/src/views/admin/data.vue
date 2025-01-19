<template>
    <div>
        <!--页面区域-->
        <div class="page-view">
            <div class="table-operations">
                <a-space>
                    <a-button type="primary" @click="handleAdd">新增</a-button>
                    <a-button @click="handleBatchDelete">批量删除</a-button>
                    <a-input-search addon-before="名称" enter-button @search="onSearch" @change="onSearchChange" />
                </a-space>
            </div>
            <a-table size="middle" rowKey="id" :loading="data.loading" :columns="columns" :data-source="data.dataList"
                :scroll="{ x: 'max-content' }" :row-selection="rowSelection" :pagination="{
                    size: 'default',
                    current: data.page,
                    pageSize: data.pageSize,
                    onChange: (current) => (data.page = current),
                    showSizeChanger: false,
                    showTotal: (total) => `共${total}条数据`,
                }">

                <template #bodyCell="{ text, record, index, column }">
                    <template v-if="column.key === 'operation'">
                        <span>
                            <a @click="handleEdit(record)">编辑</a>
                            <a-divider type="vertical" />
                            <a-popconfirm title="确定删除?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                                <a href="#">删除</a>
                            </a-popconfirm>
                        </span>
                    </template>
                </template>
            </a-table>
        </div>

        <!--弹窗区域-->
        <div>
            <a-modal :visible="modal.visile" :forceRender="true" :title="modal.title" width="880px" ok-text="确认"
                cancel-text="取消" @cancel="handleCancel" @ok="handleOk">

                <div>
                    <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form"
                        :rules="modal.rules">
                        <a-row :gutter="24">
                            <a-col span="24">
                                <a-form-item label="数据名称" name="name">
                                    <a-input placeholder="请输入" v-model:value="modal.form.name"></a-input>
                                </a-form-item>
                            </a-col>


                            <a-col span="24">
                                <a-form-item label="数据文件">
                                    <a-upload-dragger name="file" accept=".bag" :multiple="false"
                                        :before-upload="beforeUploadFile">
                                        <p class="ant-upload-text">
                                            请选择要上传数据文件
                                        </p>
                                    </a-upload-dragger>
                                </a-form-item>
                            </a-col>
<!-- 
                            <a-col span="12">
                                <a-form-item label="数据大小">
                                    <a-textarea placeholder="请输入" v-model:value="modal.form.size"></a-textarea>
                                </a-form-item>
                            </a-col> -->

                            <a-col span="24">
                                <a-form-item label="描述">
                                    <a-textarea placeholder="请输入" v-model:value="modal.form.description"></a-textarea>
                                </a-form-item>
                            </a-col>


                            <a-col span="12">
                                <a-form-item label="数据源" name="source">
                                    <a-select placeholder="请选择" allowClear v-model:value="modal.form.source">
                                        <a-select-option key="0" value="0">原始数据</a-select-option>
                                        <a-select-option key="1" value="1">仿真数据</a-select-option>
                                    </a-select>
                                </a-form-item>
                            </a-col>

                            <a-col span="12">
                                <a-form-item label="状态" name="status">
                                    <a-select placeholder="请选择" allowClear v-model:value="modal.form.status">
                                        <a-select-option key="0" value="0">正常</a-select-option>
                                        <a-select-option key="1" value="1">异常</a-select-option>
                                    </a-select>
                                </a-form-item>
                            </a-col>

                        </a-row>
                    </a-form>
                </div>
            </a-modal>
        </div>
    </div>
</template>

<script setup lang="ts">
import { FormInstance, message, SelectProps } from 'ant-design-vue';
import { createApi, listApi, updateApi, deleteApi } from '/@/api/admin/data';
import { BASE_URL } from "/@/store/constants";
import { FileImageOutlined } from '@ant-design/icons-vue';

const columns = reactive([
    {
        title: '序号',
        dataIndex: 'index',
        key: 'index',
        width: 60
    },
    {
        title: '数据名',
        dataIndex: 'name',
        key: 'name'
    },
    {
        title: '描述',
        dataIndex: 'description',
        key: 'description'
    },

    {
        title: '数据大小',
        dataIndex: 'size',
        key: 'size'
    },
    {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        customRender: ({ text, record, index, column }) => text === '0' ? '正常' : '异常'
    },

    {
        title: '来源',
        dataIndex: 'source',
        key: 'source',
        customRender: ({ text, record, index, column }) => text === '0' ? '原包' : '仿真包'
    },

    {
        title: '操作',
        dataIndex: 'action',
        key: 'operation',
        align: 'center',
        fixed: 'right',
        width: 140,
    },
]);


const beforeUploadFile = (file: File) => {
    // 改文件名
    const fileName = new Date().getTime().toString() + '.' + file.type.substring(6);
    const copyFile = new File([file], fileName);
    console.log("--copyFile--")
    console.log(copyFile);
    modal.form.file = copyFile;


    const fileSizeInMB = (file.size / 1024 / 1024).toFixed(2); // 转换为 MB 并保留两位小数
    modal.form.size = `${fileSizeInMB}MB`;
    return false;
};


// 页面数据
const data = reactive({
    dataList: [],
    loading: false,
    keyword: '',
    selectedRowKeys: [] as any[],
    pageSize: 10,
    page: 1,
});

// 弹窗数据源
const modal = reactive({
    visile: false,
    editFlag: false,
    title: '',
    cData: [],
    tagData: [{}],
    form: {
        id: undefined,
        name: undefined,
        size:undefined,
        status: undefined,
        source: undefined,
        file: undefined,
        description: undefined,
    },

    rules: {
        name: [{ required: true, message: '请输入数据名称', trigger: 'change' }],
        status: [{ required: true, message: '请选择状态', trigger: 'change' }],
        file: [{ required: true, message: '请上传数据', trigger: 'change' }]
    },
});

const myform = ref<FormInstance>();

onMounted(() => {
    getDataList();
});

const getDataList = () => {
    data.loading = true;
    listApi({
        keyword: data.keyword,
    })
        .then((res) => {
            data.loading = false;
            console.log(res);
            res.data.forEach((item: any, index: any) => {
                item.index = index + 1;
            });
            data.dataList = res.data;
        })
        .catch((err) => {
            data.loading = false;
            console.log(err);
        });
}

const onSearchChange = (e: Event) => {
    data.keyword = e?.target?.value;
    console.log(data.keyword);
};

const onSearch = () => {
    getDataList();
};

const rowSelection = ref({
    onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
        console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
        data.selectedRowKeys = selectedRowKeys;
    },
});

const handleAdd = () => {
    resetModal();
    modal.visile = true;
    modal.editFlag = false;
    modal.title = '新增';
    // 重置
    for (const key in modal.form) {
        modal.form[key] = undefined;
    }

};

const handleEdit = (record: any) => {
    resetModal();
    modal.visile = true;
    modal.editFlag = true;
    modal.title = '编辑';
    // 重置
    for (const key in modal.form) {
        modal.form[key] = undefined;
    }
    for (const key in record) {
        if (record[key]) {
            modal.form[key] = record[key];
        }
    }
};

const confirmDelete = (record: any) => {
    console.log('delete', record);
    deleteApi({ ids: record.id })
        .then((res) => {
            getDataList();
        })
        .catch((err) => {
            message.error(err.msg || '操作失败');
        });
};

const handleBatchDelete = () => {
    console.log(data.selectedRowKeys);
    if (data.selectedRowKeys.length <= 0) {
        console.log('hello');
        message.warn('请勾选删除项');
        return;
    }
    deleteApi({ ids: data.selectedRowKeys.join(',') })
        .then((res) => {
            message.success('删除成功');
            data.selectedRowKeys = [];
            getDataList();
        })
        .catch((err) => {
            message.error(err.msg || '操作失败');
        });
};

const handleOk = () => {
    myform.value
        ?.validate()
        .then(() => {
            const formData = new FormData();
            if (modal.editFlag) {
                formData.append('id', modal.form.id)
            }
            formData.append('name', modal.form.name)
            formData.append('size', modal.form.size)
            formData.append('status', modal.form.status)
            formData.append('source', modal.form.source)
            if (modal.form.file) {
                formData.append('file', modal.form.file)
            }

            formData.append('description', modal.form.description || '')


            if (modal.editFlag) {
                updateApi({
                    id: modal.form.id
                }, formData)
                    .then((res) => {
                        hideModal();
                        getDataList();
                    })
                    .catch((err) => {
                        console.log(err);
                        message.error(err.msg || '操作失败');
                    });
            } else {
                createApi(formData)
                    .then((res) => {
                        hideModal();
                        getDataList();
                    })
                    .catch((err) => {
                        console.log(err);
                        message.error(err.msg || '操作失败');
                    });
            }
        })
        .catch((err) => {
            console.log('不能为空');
        });
};


const handleCancel = () => {
    hideModal();
};

// 恢复表单初始状态
const resetModal = () => {
    myform.value?.resetFields();

};

// 关闭弹窗
const hideModal = () => {
    modal.visile = false;
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

.table-operations {
    margin-bottom: 16px;
    text-align: right;
}

.table-operations>button {
    margin-right: 8px;
}
</style>