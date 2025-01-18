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
          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="24">
                <a-form-item label="算法名称" name="title">
                  <a-input placeholder="请输入" v-model:value="modal.form.title"></a-input>
                </a-form-item>
              </a-col>

              <a-col span="24">
                <a-form-item label="评测维度">
                  <a-select mode="multiple" placeholder="请选择" allowClear v-model:value="modal.form.type">
                    <template v-for="item in modal.typeData">
                      <a-select-option :value="item.id">{{ item.title }}</a-select-option>
                    </template>
                  </a-select>
                </a-form-item>
              </a-col>

              <a-col span="24">
                <a-form-item label="算法原理图">
                  <a-upload-dragger name="file" accept="image/*" :multiple="false" :before-upload="beforeUploadImage">
                    <p class="ant-upload-text">
                      请选择要上传的算法原理图
                    </p>
                  </a-upload-dragger>
                </a-form-item>
              </a-col>


              <a-col span="24">
                <a-form-item label="算法文件">
                  <a-upload-dragger name="file" accept=".exe" :multiple="false" :before-upload="beforeUploadFile">
                    <p class="ant-upload-text">
                      请选择要上传的算法文件
                    </p>
                  </a-upload-dragger>
                </a-form-item>
              </a-col>

              <a-col span="24">
                <a-form-item label="简介">
                  <a-textarea placeholder="请输入" v-model:value="modal.form.description"></a-textarea>
                </a-form-item>
              </a-col>

              <a-col span="12">
                <a-form-item label="开发状态" name="status">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.status">
                    <a-select-option key="0" value="0">已完成</a-select-option>
                    <a-select-option key="1" value="1">开发中</a-select-option>
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

import { createApi, listApi, updateApi, deleteApi } from '/@/api/admin/algorithm';

import { listApi as listTypeApi } from '/@/api/admin/type'

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
    title: '标题',
    dataIndex: 'title',
    key: 'title'
  },

  {
    title: '标签',
    dataIndex: 'label',
    key: 'label'
  },

  {
    title: '开发状态',
    dataIndex: 'status',
    key: 'status',
    customRender: ({ text, record, index, column }) => text === '0' ? '已完成' : '开发中'
  },

  {
    title: '简介',
    dataIndex: 'description',
    key: 'description',
    customRender: ({ text, record, index, column }) => text ? text.substring(0, 10) + '...' : '--'
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


const beforeUploadFile = (file) => {
  const isExe = file.type === 'application/x-msdownload' || file.name.endsWith('.exe');
  if (!isExe) {
    message.error('你只能上传EXE文件!');
    return false;
  }
  const isLt10M = file.size / 1024 / 1024 < 10;
  if (!isLt10M) {
    message.error('文件必须小于 10MB!');
    return false;
  }
  // 改文件名
  const fileName = new Date().getTime().toString() + '.exe';
  const copyFile = new File([file], fileName);
  console.log("--beforeUploadFile--");
  console.log(copyFile);
  modal.form.file = copyFile;
  return false;
};

const beforeUploadImage = (file: File) => {
  // 改文件名
  const fileName = new Date().getTime().toString() + '.' + file.type.substring(6);
  const copyFile = new File([file], fileName);
  console.log("--beforeUploadImage--")
  console.log(copyFile);
  modal.form.imageFile = copyFile;
  return false;
};


// // 文件列表
// const imageList = ref<any[]>([]);
// const fileList = ref<any[]>([]);

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
  typeData: [{}],
  form: {
    id: undefined,
    title: undefined,
    description: undefined,
    status: undefined,
    type: [],
    // imageFile: undefined,
    // file: undefined,
  },

  rules: {
    title: [{ required: true, message: '请输入算法标题', trigger: 'change' }],
    description: [{ required: true, message: '请输入算法描述', trigger: 'change' }],
    status: [{ required: true, message: '请选择算法开发状态', trigger: 'change' }],
    // file: [{ required: true, message: '请上传算法文件', trigger: 'change' }]
  },
});

const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
  getTypeDataList();
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



const getTypeDataList = () => {
  listTypeApi({}).then(res => {

    res.data.forEach((item, index) => {
      item.index = index + 1
    })
    modal.typeData = res.data
  })
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
  modal.form.cover = undefined
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
      formData.append('title', modal.form.title)
      formData.append('description', modal.form.description || '')
      if (modal.form.status) {
        formData.append('status', modal.form.status)
      }
      if (modal.form.type) {
        modal.form.type.forEach(function (value) {
          if (value) {
            formData.append('type', value)
          }
        })
      }
      if (modal.form.imageFile) {
        formData.append('image', modal.form.imageFile)
      }
      // if (modal.form.file) {
      //   formData.append('file', modal.form.file)
      // }
      
      console.log("---algorithm formData---")
      console.log(formData)
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
  // imageList.value = []
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