<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-setting"></i> 管理</el-breadcrumb-item>
                <el-breadcrumb-item>课程信息列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div>
            <el-table :data="data" border style="width: 90%" ref="multipleTable" >
                <el-table-column label="课程号" prop="cno" width="200px" ></el-table-column>
                <el-table-column label="课程名称" prop="cname" width="200px" ></el-table-column>
                <el-table-column label="前置课程号" prop="cpno" width="150px" ></el-table-column>
                <el-table-column label="学分" prop="ccredit" width="150px" ></el-table-column>
                <el-table-column label="操作" width="200px" >
                    <template slot-scope="scope" width="100px">
                        <el-button type="text" @click="openedit(scope.row)" >修改</el-button>
                        <el-button type="text" @click="del_user(scope.row)" >删除</el-button>
                    </template>
                </el-table-column>
            </el-table><el-button type="primary" @click="adduser()" align="center">添加课程</el-button>
            <template>
            </template>
        </div>
        <el-dialog
            width="30%"
            title="更新课程信息"
            :visible.sync="dialogFormVisibleed">
            <div class="form-box">
                <el-form :model="form"  ref="form" label-width="150px">
                    <el-form-item label="课程号" prop="cno">
                        <el-input v-model="form.cno" placeholder="请输入课程号"></el-input>
                    </el-form-item>
                    <el-form-item label="课程名称" prop="cname">
                        <el-input v-model="form.cname" placeholder="请输入课程名称"></el-input>
                    </el-form-item>
                    <el-form-item label="前置课程课号" prop="cpno">
                        <el-input v-model="form.cpno"  placeholder="请输入前置课程课号"></el-input>
                    </el-form-item>
                    <el-form-item label="学分" prop="ccredit">
                        <el-input v-model="form.ccredit"  placeholder="请输入本课程学分"></el-input>
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
            title="添加课程"
            :visible.sync="dialogFormVisibleed1">
            <div class="form-box">
                <el-form :model="form" :rules="rules1" ref="form" label-width="150px">
                    <el-form-item label="课程号" prop="cno">
                        <el-input v-model="form.cno" placeholder="请输入课程号"></el-input>
                    </el-form-item>
                    <el-form-item label="课程名称" prop="cname">
                        <el-input v-model="form.cname" placeholder="请输入课程名称"></el-input>
                    </el-form-item>
                    <el-form-item label="前置课程课号" prop="cpno">
                        <el-input v-model="form.cpno"  placeholder="请输入前置课程课号"></el-input>
                    </el-form-item>
                    <el-form-item label="学分" prop="ccredit">
                        <el-input v-model="form.ccredit"  placeholder="请输入学分"></el-input>
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
        var checkpasswd = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次确认新密码'));
            } else if (value !== this.form.password1) {
                callback(new Error('两次输入的新密码不一致!'));
            } else {
                callback();
            }
        };
        var checkuser = (rule, value, callback) => {
            for(let i=0;i<this.data.length;i++){
                if(this.data[i].cno === value){
                    this.form.ban = '1';
                    callback(new Error('该课程号已存在'));
                }
            }
        };
        return {
            data:[],
            dialogFormVisibleed:false,
            dialogFormVisibleed1:false,
            form:{
                cno:'',
                cname:'',
                cpno:'',
                ccredit:'',
                ban:'0' //重名检测，用户名是否已经存在，0存在1不存在
            },
            rules1:{
                cno:[
                    {required:true, message:'请输入课程号',trigger:'blur'},
                    { validator: checkuser, trigger: 'blur'}
                ],
                cname:[
                    {required:true, message:'请输入课程名称',trigger:'blur'}
                ],
                cpno:[
                    {required:false, message:'请输入前置课程号',trigger:'blur'},
                ],
                ccredit:[
                    {required:true, message:'请输入课程学分',trigger:'blur'}
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
            this.$http.post(main.url+"/course/course_list").then(
                success=>{
                    this.data=success.data;
                }
            )
        },
        openedit(row){
            this.dialogFormVisibleed=true;
            this.form={
                cname:row.cname,
                cno:row.cno,
                cpno:row.cpno,
                ccredit: row.ccredit
                // role: 0
            };
        },
        update_submit(form){ //更新课程信息
            if(this.form.cno==="")
                this.$message({type: 'error', message: '课程号不能为空！1'});
            else {
                this.$http.post(main.url+"/course/course_update",
                    {
                        'cno': this.form.cno,
                        'cname': this.form.cname,
                        'cpno': this.form.cpno,
                        'ccredit': this.form.ccredit
                    },
                    {
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        emulateJSON: true
                    }).then(
                    response => {
                        if(response.data === '1'){
                            this.$message({type: 'success', message: '更新成功'});
                            this.form = {
                                cno:'',
                                cname:'',
                                cpno:'',
                                ccredit:'',
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
                cno:'',
                cname:'',
                cpno:'',
                ccredit:'',
                ban:'0'
            };
            this.dialogFormVisibleed1=true
        },
        adduser_submit(form){ //添加新用户
            if(this.form.cno==="")
                this.$message({type: 'error', message: '课程号不能为空！'});
            else if(this.form.ban==="1")
                this.$message({type: 'error', message: '课程已存在！'});
            else {
                this.$http.post(main.url+"/course/course_insert",
                    {
                        'cno': this.form.cno,
                        'cname': this.form.cname,
                        'cpno': this.form.cpno,
                        'ccredit': this.form.ccredit
                    },
                    {
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        emulateJSON: true
                    }).then(
                    response => {
                        if(response.data === '1'){
                            this.$message({type: 'success', message: '添加成功'});
                            this.form = {
                                cno:'',
                                cname:'',
                                cpno:'',
                                ccredit:'',
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
        del_user(row){  //删除课程
            if(row.username === localStorage.getItem('username'))
                this.$message({type: 'info', message: '不能删除自己！'});
            else{
                this.$confirm('请确认是否要删除该课程！', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post(main.url+"/course/course_delete",
                        {'cno': row.cno,},
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
