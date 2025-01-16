<template>
    <div>
        <!--页面区域-->
        <div class="page-view">
            <div class="table-operations">
                <a-space>
                    <a-button type="primary" @click="handleAdd">新增</a-button>
                    <a-button @click="handleBatchDelete">批量删除</a-button>
                </a-space>
            </div>

            <a-table size="middle" rowKey="id" :loading="data.loading" :columns="columns" :data-source="data.userList"
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
        <!--弹窗区域，绑定model属性到a-model组件-->
        <div>

            <a-modal :visible="modal.visile" :forceRender="true" :title="modal.title" ok-text="确认" cancel-text="取消"
                @cancel="handleCancel" @ok="handleOk">
                <div>
                    <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form"
                        :rules="modal.rules">
                        <a-row :gutter="24">
                            <a-col span="24">
                                <a-form-item label="算法名称" name="title">
                                    <a-input placeholder="请输入" v-model:value="modal.form.title"></a-input>
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
import { FormInstance, message } from 'ant-design-vue';
import { createApi, listApi, updateApi, deleteApi } from '/@/api/admin/task';

// 指定列对应的数据字段名称
const columns = reactive([
    {
        title: '任务标题',
        dataIndex: 'title',
        key: 'title',
    },
    {
        title: '任务描述',
        dataIndex: 'description',
        key: 'description',
    },
    {
        title: '使用数据',
        dataIndex: 'ros',
        key: 'ros',
    },
    {
        title: '算法',
        dataIndex: 'algorithm',
        key: 'algorithm',
    },

    {
        title: '任务结果',
        dataIndex: 'evaluate_result',
        key: 'evaluate_result',
    },
    
    { title: '创建时间', dataIndex: 'create_time', key: 'create_time' },
 
    {
        title: '操作',
        dataIndex: 'action',
        key: 'operation',
        align: 'center',
        fixed: 'right',
        width: 140,
    },
]);

const data = reactive({
    userList: [],
    loading: false,
    currentAdminUserName: '',
    keyword: '',
    selectedRowKeys: [] as any[],
    pageSize: 5,
    page: 1,
});

// 弹窗数据源
const modal = reactive({
    visile: false,
    editFlag: false,
    title: '',
    form: {
        id: undefined,
        key: undefined,
        title: undefined,
    },
    rules: {
        title: [{ required: true, message: '请输入', trigger: 'change' }],
    },
});

const myform = ref<FormInstance>();

onMounted(() => {
    getDataList();
});

// getDataList方法用于从服务器获取数据并填充到表格中。
const getDataList = () => {
    data.loading = true;
    listApi({
        keyword: data.keyword,
    })
        .then((res) => {
            data.loading = false;
            console.log('API Response:', res);
            console.log('API Response data:', res.data);
            res.data.forEach((item: any, index: any) => {
                item.index = index + 1;
            });
            data.userList = res.data;
        })
        .catch((err) => {
            data.loading = false;
            console.log(err);
        });
};


const rowSelection = ref({
    onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
        console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
        data.selectedRowKeys = selectedRowKeys;
        console.log("data.selectedRowKeys--" + data.selectedRowKeys)
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


const handleEdit = (record) => {
    console.log("--handleEdit---")
    console.log(record)
    resetModal();
    modal.visile = true;
    modal.editFlag = true;
    modal.title = '编辑';
    // 重置

    for (const key in modal.form) {
        modal.form[key] = undefined;
    }

    for (const key in record) {
        console.log("key: " + key)
        modal.form[key] = record[key];
    }
};

const confirmDelete = (record: any) => {
    console.log('delete', record);
    deleteApi({ ids: record.id })
        .then((res) => {
            getDataList();
        })
        .catch((err) => {
            message.error(err.msg || '删除失败');
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
            message.error(err.msg || '删除失败');
        });
};

// async+await形式
const handleOk = async () => {
    try {
        await myform.value?.validate();
        if (modal.editFlag) {
            try {
                const res = await updateApi({ id: modal.form.id }, modal.form);
                hideModal();
                getDataList();
            } catch (err) {
                console.log(err);
                message.error(err.msg || '操作失败');
            }
        } else {
            try {
                const res = await createApi(modal.form);
                hideModal();
                getDataList();
            } catch (err) {
                console.log(err);
                message.error(err.msg || '操作失败');
            }
        }
    } catch (err) {
        console.log('不能为空');
    }
};


// 原始回调地狱
const handleOk_old = () => {
    myform.value
        ?.validate()
        .then(() => {
            if (modal.editFlag) {
                updateApi({ id: modal.form.id }, modal.form)
                    .then((res) => {
                        hideModal();
                        getDataList();
                    })
                    .catch((err) => {
                        console.log(err);
                        message.error(err.msg || '操作失败');

                    });
            } else {
                createApi(modal.form)
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