<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-setting"></i> 管理</el-breadcrumb-item>
                <el-breadcrumb-item>学生信息列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div>
            <el-table :data="data" border style="width: 90%" ref="multipleTable" >
                <el-table-column label="学号" prop="sno" width="200px" ></el-table-column>
                <el-table-column label="姓名" prop="sname" width="200px" ></el-table-column>
                <el-table-column label="性别" prop="ssex" width="150px" ></el-table-column>
                <el-table-column label="年龄" prop="sage" width="150px" ></el-table-column>
                <el-table-column label="所在院系" prop="sdept" width="150px" ></el-table-column>
                <el-table-column label="操作" width="200px" >
                    <template slot-scope="scope" width="100px">
                        <el-button type="text" @click="openedit(scope.row)" >修改</el-button>
                        <el-button type="text" @click="del_user(scope.row)" >删除</el-button>
                    </template>
                </el-table-column>
            </el-table><el-button type="primary" @click="adduser()" align="center">添加学生</el-button>
            <template>
            </template>
        </div>
        <el-dialog
            width="30%"
            title="更新学生信息"
            :visible.sync="dialogFormVisibleed">
            <div class="form-box">
                <el-form :model="form"  ref="form" label-width="150px">
                    <el-form-item label="学号" prop="sno">
                        <el-input v-model="form.sno" placeholder="请输入学号"></el-input>
                    </el-form-item>
                    <el-form-item label="姓名" prop="sname">
                        <el-input v-model="form.sname" placeholder="请输入姓名"></el-input>
                    </el-form-item>
                    <el-form-item label="性别" prop="ssex">
                        <el-select v-model="form.ssex" placeholder="请选择性别">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="年龄" prop="sage">
                        <el-input v-model="form.sage"  placeholder="请输入年龄"></el-input>
                    </el-form-item>
                    <el-form-item label="院系" prop="sdept">
                        <el-input v-model="form.sdept"  placeholder="请输入院系"></el-input>
                    </el-form-item>
                    <el-form-item style="text-align: center" >
                        <el-button @click="dialogFormVisibleed = false" >取 消</el-button>
                        <el-button type="primary" @click="update_submit(form)">更新</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-dialog>
        <el-dialog
            width="30%"
            title="添加学生"
            :visible.sync="dialogFormVisibleed1">
            <div class="form-box">
                <el-form :model="form" :rules="rules1" ref="form" label-width="150px">
                    <el-form-item label="学号" prop="sno">
                        <el-input v-model="form.sno" placeholder="请输入学号"></el-input>
                    </el-form-item>
                    <el-form-item label="姓名" prop="sname">
                        <el-input v-model="form.sname" placeholder="请输入姓名"></el-input>
                    </el-form-item>
                    <el-form-item label="性别" prop="ssex">
                        <el-select v-model="form.ssex" placeholder="请选择性别">
                            <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="年龄" prop="sage">
                        <el-input v-model="form.sage"  placeholder="请输入年龄"></el-input>
                    </el-form-item>
                    <el-form-item label="院系" prop="sdept">
                        <el-input v-model="form.sdept"  placeholder="请输入院系"></el-input>
                    </el-form-item>
                    <el-form-item style="text-align: center" >
                        <el-button @click="dialogFormVisibleed1 = false" >取 消</el-button>
                        <el-button type="primary" @click="adduser_submit(form)">添加</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    import main from "../../main";
    export default {
        data: function(){
            var checkuser = (rule, value, callback) => {
                for(let i=0;i<this.data.length;i++){
                    if(this.data[i].sno === value){
                        this.form.ban = '1';
                        callback(new Error('该学号已存在'));
                    }
                }
            };
            return {
                data:[],
                dialogFormVisibleed:false,
                dialogFormVisibleed1:false,
                options:[{value: '男', label: "男"},{value: '女', label: "女"}],
                form:{
                    sno:'',
                    sname:'',
                    ssex:'',
                    sage:'',
                    sdept: '',
                    ban:'0' //重名检测，用户名是否已经存在，0存在1不存在
                },
                rules1:{
                    sno:[
                        {required:true, message:'请输入学号',trigger:'blur'},
                        { validator: checkuser, trigger: 'blur'}
                    ],
                    sname:[
                        {required:true, message:'请输入姓名',trigger:'blur'}
                    ],
                    ssex:[
                        {required:true, message:'请输入性别',trigger:'blur'},
                    ],
                    sage:[
                        {required:true, message:'请输入年龄',trigger:'blur'}
                    ],
                    sdept:[
                        {required:true, message:'请输入院系',trigger:'blur'}
                    ]
                },
            }
        },
        created(){
            if(localStorage.getItem('username') != "admin"){
                this.$router.replace('/login');
            }
            else{this.init();}
        },
        methods:{
            init(){
                this.$http.post(main.url+"/student/stu_list").then(
                    success=>{
                        this.data=success.data;
                    }
                )
            },
            openedit(row){
                this.dialogFormVisibleed=true;
                this.form={
                    sname:row.sname,
                    ssex:row.ssex,
                    sdept: row.sdept,
                    sage : row.sage,
                    sno: row.sno,
                    // role: 0
                };
            },
            update_submit(form){ //更新学生信息
                if(this.form.sname==="")
                    this.$message({type: 'error', message: '用户名不能为空！'});
                else {
                    this.$http.post(main.url+"/student/stu_update",
                        {
                            'sno': this.form.sno,
                            'sname': this.form.sname,
                            'ssex': this.form.ssex,
                            'sage': this.form.sage,
                            'sdept': this.form.sdept
                        },
                        {
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                            emulateJSON: true
                        }).then(
                        response => {
                            if(response.data === '1'){
                                this.$message({type: 'success', message: '更新成功'});
                                this.form = {
                                    sno:'',
                                    sname:'',
                                    ssex:'',
                                    sage:'',
                                    sdept: '',
                                    ban:'0'
                                };
                                this.init();
                            }else {
                                this.$message({ type: 'error', message: '更新失败，请重试' });
                            }

                        }
                    );
                    this.dialogFormVisibleed = false
                }
            },
            adduser(){
                this.form = {
                    sno:'',
                    sname:'',
                    ssex:'',
                    sage:'',
                    sdept: '',
                    ban:'0'
                };
                this.dialogFormVisibleed1=true
            },
            adduser_submit(form){ //添加新用户
                if(this.form.sname==="")
                    this.$message({type: 'error', message: '用户名不能为空！'});
                // else if(this.form.password1!==this.form.password2)
                //     this.$message({type: 'error', message: '两次密码不一样！'});
                else if(this.form.ban==="1")
                    this.$message({type: 'error', message: '学号已存在！'});
                else {
                    this.$http.post(main.url+"/student/stu_insert",
                        {
                            'sno': this.form.sno,
                            'sname': this.form.sname,
                            'ssex': this.form.ssex,
                            'sage': this.form.sage,
                            'sdept': this.form.sdept

                        },
                        {
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                            emulateJSON: true
                        }).then(
                        response => {
                            if(response.data === '1'){
                                this.$message({type: 'success', message: '添加成功'});
                                this.form = {
                                    sno:'',
                                    sname:'',
                                    ssex:'',
                                    sage:'',
                                    sdept: 0,
                                    ban:'0'
                                };
                                this.init();
                            }else {
                                this.$message({ type: 'error', message: '添加失败，请重试' });
                            }

                        }
                    );
                    this.dialogFormVisibleed1 = false
                }
            },
            del_user(row){  //删除用户
                if(row.username === localStorage.getItem('username'))
                    this.$message({type: 'info', message: '不能删除自己！'});
                else{
                    this.$confirm('请确认是否要删除该用户！', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    }).then(() => {
                        this.$http.post(main.url+"/student/stu_delete",
                            {'sno': row.sno,},
                            {
                                headers: {'Content-Type':'application/x-www-form-urlencoded'},
                                emulateJSON: true
                            }).then(
                            response => {
                                if(response.data === '1'){
                                    this.$message({type: 'success', message: '已删除'});
                                    this.init();
                                }else {
                                    this.$message({ type: 'error', message: '删除失败，请重试' });
                                }
                            }
                        );
                    }).catch(() => {
                        this.$message({type: 'info', message: '已取消'});
                    });
                }
            },
        }
    }
</script>
