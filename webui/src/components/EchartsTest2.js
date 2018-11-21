import React, { Component } from 'react';

// 引入 ECharts 主模块
import echarts from 'echarts/lib/echarts';
// 引入柱状图
import 'echarts/lib/chart/bar';
import 'echarts/lib/chart/line';
// 引入提示框和标题组件
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import 'echarts/lib/component/markLine';

class EchartsTest2 extends Component {
    componentDidMount() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main_echarttest2'));


        let option = { 
            title : {
                        left: 'center',
                        show: false
                    },
                    grid: {
                        left: '3%',
                        right: '5%',
                        bottom: '5%',
                        containLabel: true
                    },
                    tooltip : {
                        showDelay : 0,
                        formatter : function (params) { //格式化鼠标移上去显示内容样式
                            if (params.value.length > 1) {
                                return params.value[2] ;
                            }
                            
                        },
                        backgroundColor: '#fff', //气泡背景色
                        textStyle: { //文字样式
                            color: '#333'
                        },
                        borderColor:'#CBCBCB',//气泡边框颜色
                        borderWidth:1,//气泡边框款
                        extraCssText: 'box-shadow: 0 0 3px rgba(0, 0, 0, 0.3);'//API中的让气泡带有阴影的效果
                    },
                    xAxis : [
                        {
                            type : 'value',
                            scale:false,
                            axisLabel : {
                                formatter: '{value}%'
                            },
                            axisTick:{ //刻度线样式
                                show: false
                            }
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value',
                            scale:false,
                            axisLabel : {
                                formatter: '{value}'
                            },
                            axisTick:{
                                show: false
                            }
                        }
                    ],
                    series : [
                        {
                            type:'scatter',
                            data:  [
                                    [10.0, 8.04,'point1'],
                                    [8.0, 6.95,'point2'],
                                    [13.0, 7.58,'point3'],
                                    [9.0, 8.81,'point4'],
                                    [11.0, 8.33,'point5']
                                ],
                            itemStyle:{ //当前数据的样式
                              normal:{color:'#556EAA'}
                          }
                        },
                        {
                            type:'scatter',
                            data:  [
                                    [10.0, 11.2,'point6'],
                                    [12.5, 16.3,'point7'],
                                    [14.1, 10.2,'point8'],
                                    [11.0, 12.0,'point9'],
                                    [11.0, 13.1,'point10']
                                ],
                            itemStyle:{
                              normal:{color:'#DB442D'}
                            },
                            markLine : {//标记线设置
                                lineStyle: {
                                    normal: {
                                        type: 'solid'
                                    }
                                },
                                symbolSize:0,//控制箭头和原点的大小、官方默认的标准线会带远点和箭头
                                data : [ //设置两条标准线——x=10 和 y=10
                                    { xAxis: 10 },
                                    { yAxis: 10 }
                                ]
                            }
                        }
                    ]
                 };


        // 绘制图表
        myChart.setOption(option);
    }
    render() {
        return (
            <div id="main_echarttest2" style={{ width: 400, height: 400 }}></div>
        );
    }
}

export default EchartsTest2;