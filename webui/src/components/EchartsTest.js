import React, { Component } from 'react';

// 引入 ECharts 主模块
import echarts from 'echarts/lib/echarts';
// 引入柱状图
import 'echarts/lib/chart/bar';
import 'echarts/lib/chart/line';
// 引入提示框和标题组件
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';

class EchartsTest extends Component {
    componentDidMount() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main_echarttest'));

        let option = {
            title : {
                text: '未来一周气温变化',
                subtext: '纯属虚构'
            },
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data:['最高气温','最低气温']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {show: true, type: ['line', 'bar']},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            xAxis : [
                {
                    type : 'category',
                    boundaryGap : false,
                    data : [1,2,3,4,5,6,7]
                }
            ],
            yAxis : [
                {
                    type : 'value',
                    axisLabel : {
                        formatter: '{value} °C'
                    }
                }
            ],
            series : [
                {
                    name:'最高气温',
                    type:'line',
                    data:[11, 11, 15, 13, 12, 13, 10],
                    markPoint : {
                        data : [
                            {type : 'max', name: '最大值'},
                            {type : 'min', name: '最小值'}
                        ]
                    }
                    ,
                    markLine : {
                        data : [
                           
                            [
                            {
                                name: '两个坐标之间的标线',
                                coord: [1, 10]
                            },
                            {
                                coord: [3, 12]
                            }
                            ]
                        ]
                    }
                },
                {
                    name:'最低气温',
                    type:'line',
                    data:[1, -2, 2, 5, 3, 2, 0],
                    markPoint : {
                        data : [
                            {name : '周最低', value : -2, xAxis: 1, yAxis: -1.5}
                        ]
                    },
                    markLine : {
                        data : [
                            {type : 'average', name : '平均值'}
                        ]
                    }
                }
            ]
        };
                                    

        // let option = {
        //     title: {
        //         text: '某楼盘销售情况',
        //         subtext: '纯属虚构'
        //     },
        //     tooltip: {
        //         trigger: 'axis'
        //     },
        //     legend: {
        //         data: ['意向', '预购', '成交']
        //     },
        //     toolbox: {
        //         show: true,
        //         feature: {
        //             mark: { show: true },
        //             dataView: { show: true, readOnly: false },
        //             magicType: { show: true, type: ['line', 'bar', 'stack', 'tiled'] },
        //             restore: { show: true },
        //             saveAsImage: { show: true }
        //         }
        //     },
        //     calculable: true,
        //     xAxis: [
        //         {
        //             type: 'category',
        //             boundaryGap: false,
        //             data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        //         }
        //     ],
        //     yAxis: [
        //         {
        //             type: 'value'
        //         }
        //     ],
        //     series: [
        //         {
        //             name: '成交',
        //             type: 'line',
        //             smooth: true,
        //             itemStyle: { normal: { areaStyle: { type: 'default' } } },
        //             data: [10, 12, 21, 54, 260, 830, 710],
        //             markLine: {
        //                 // itemStyle: {  //solid
        //                 //     normal: { lineStyle: { type: 'line', color: '#FFF' }, label: { show: true, position: 'left' } }
        //                 // },
        //                 // large: true,
        //                 // effect: {
        //                 //     show: false,
        //                 //     loop: true,
        //                 //     period: 0,
        //                 //     scaleSize: 2,
        //                 //     color: null,
        //                 //     shadowColor: null,
        //                 //     shadowBlur: null
        //                 // },
        //                 data: [
        //                     [
        //                         { name: '标线1起点', value: 400, xAxis: -1, yAxis: 400 },      // 当xAxis为类目轴时，数值1会被理解为类目轴的index，通过xAxis:-1|MAXNUMBER可以让线到达grid边缘
        //                         { name: '标线1终点', xAxis: '周日', yAxis: 400 },             // 当xAxis为类目轴时，字符串'周三'会被理解为与类目轴的文本进行匹配
        //                     ],
        //                 ]
        //             }



        //         },
        //         {
        //             name: '预购',
        //             type: 'line',
        //             smooth: true,
        //             itemStyle: { normal: { areaStyle: { type: 'default' } } },
        //             data: [30, 182, 434, 791, 390, 30, 10]
        //         },
        //         {
        //             name: '意向',
        //             type: 'line',
        //             smooth: true,
        //             itemStyle: { normal: { areaStyle: { type: 'default' } } },
        //             data: [1320, 1132, 601, 234, 120, 90, 20]
        //         }
        //     ]
        // };

        // ----------------------------------------------------------------------------------

        // let option = {
        //     tooltip: {
        //         trigger: 'axis'
        //     },
        //     legend: {
        //         data: ['邮件营销', '联盟广告', '直接访问', '搜索引擎']
        //     },
        //     toolbox: {
        //         show: true,
        //         feature: {
        //             mark: { show: true },
        //             dataView: { show: true, readOnly: false },
        //             magicType: { show: true, type: ['line', 'bar', 'stack', 'tiled'] },
        //             restore: { show: true },
        //             saveAsImage: { show: true }
        //         }
        //     },
        //     calculable: true,
        //     xAxis: [
        //         {
        //             type: 'category',
        //             boundaryGap: false,
        //             data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        //         }
        //     ],
        //     yAxis: [
        //         {
        //             type: 'value'
        //         }
        //     ],
        //     series: [
        //         {
        //             name: '邮件营销',
        //             type: 'line',
        //             stack: '总量',
        //             symbol: 'none',
        //             itemStyle: {
        //                 normal: {
        //                     areaStyle: {
        //                         // 区域图，纵向渐变填充
        //                         color: 'orange'
        //                         // color: (function () {
        //                         //     var zrColor = require('zrender/tool/color');
        //                         //     return zrColor.getLinearGradient(
        //                         //         0, 200, 0, 400,
        //                         //         [[0, 'rgba(255,0,0,0.8)'], [0.8, 'rgba(255,255,255,0.1)']]
        //                         //     )
        //                         // })()
        //                     }
        //                 }
        //             },
        //             data: [
        //                 120, 132, 301, 134,
        //                 { value: 90, symbol: 'droplet', symbolSize: 5 },
        //                 230, 210
        //             ]
        //         },
        //         {
        //             name: '联盟广告',
        //             type: 'line',
        //             stack: '总量',
        //             smooth: true,
        //             symbol: 'image://../asset/ico/favicon.png',     // 系列级个性化拐点图形
        //             symbolSize: 8,
        //             markLine : {
        //                 data : [
        //                     {name: '标线1起点', value: 500, x: '周一', y: 400},
        //                     {name: '标线1终点', x: '周五', y: 400}
        //                 ]
        //             },
        //             data: [
        //                 120, 82,
        //                 {
        //                     value: 201,
        //                     symbol: 'star',  // 数据级个性化拐点图形
        //                     symbolSize: 15,
        //                     itemStyle: {
        //                         normal: {
        //                             label: {
        //                                 show: true,
        //                                 textStyle: {
        //                                     fontSize: '20',
        //                                     fontFamily: '微软雅黑',
        //                                     fontWeight: 'bold'
        //                                 }
        //                             }
        //                         }
        //                     }
        //                 },
        //                 {
        //                     value: 134,
        //                     symbol: 'none'
        //                 },
        //                 190,
        //                 {
        //                     value: 230,
        //                     symbol: 'emptypin',
        //                     symbolSize: 8
        //                 },
        //                 110
        //             ]
        //         },
        //         {
        //             name: '直接访问',
        //             type: 'line',
        //             stack: '总量',
        //             symbol: 'arrow',
        //             symbolSize: 6,
        //             symbolRotate: -45,
        //             itemStyle: {
        //                 normal: {
        //                     color: 'red',
        //                     lineStyle: {        // 系列级个性化折线样式
        //                         width: 2,
        //                         type: 'dashed'
        //                     }
        //                 },
        //                 emphasis: {
        //                     color: 'blue'
        //                 }
        //             },
        //             data: [
        //                 320, 332, '-', 334,
        //                 {
        //                     value: 390,
        //                     symbol: 'star6',
        //                     symbolSize: 20,
        //                     symbolRotate: 10,
        //                     itemStyle: {        // 数据级个性化折线样式
        //                         normal: {
        //                             color: 'yellowgreen'
        //                         },
        //                         emphasis: {
        //                             color: 'orange',
        //                             label: {
        //                                 show: true,
        //                                 position: 'inside',
        //                                 textStyle: {
        //                                     fontSize: '20'
        //                                 }
        //                             }
        //                         }
        //                     }
        //                 },
        //                 330, 320
        //             ]
        //         },
        //         {
        //             name: '搜索引擎',
        //             type: 'line',
        //             symbol: 'emptyCircle',
        //             itemStyle: {
        //                 normal: {
        //                     lineStyle: {            // 系列级个性化折线样式，横向渐变描边
        //                         width: 2,
        //                         color: 'orange',
        //                         // color: (function () {
        //                         //     var zrColor = require('zrender/tool/color');
        //                         //     return zrColor.getLinearGradient(
        //                         //         0, 0, 1000, 0,
        //                         //         [[0, 'rgba(255,0,0,0.8)'], [0.8, 'rgba(255,255,0,0.8)']]
        //                         //     )
        //                         // })(),
        //                         shadowColor: 'rgba(0,0,0,0.5)',
        //                         shadowBlur: 10,
        //                         shadowOffsetX: 8,
        //                         shadowOffsetY: 8
        //                     }
        //                 },
        //                 emphasis: {
        //                     label: { show: true }
        //                 }
        //             },
        //             data: [
        //                 620, 732, 791,
        //                 { value: 734, symbol: 'emptyHeart', symbolSize: 10 },
        //                 890, 930, 820
        //             ]
        //         }
        //     ]
        // };



        // 绘制图表
        myChart.setOption(option);
    }
    render() {
        return (
            <div id="main_echarttest" style={{ width: 400, height: 400 }}></div>
        );
    }
}

export default EchartsTest;