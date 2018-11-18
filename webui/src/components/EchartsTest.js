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
        var myChart = echarts.init(document.getElementById('main'));


        let option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['邮件营销', '联盟广告', '直接访问', '搜索引擎']
            },
            toolbox: {
                show: true,
                feature: {
                    mark: { show: true },
                    dataView: { show: true, readOnly: false },
                    magicType: { show: true, type: ['line', 'bar', 'stack', 'tiled'] },
                    restore: { show: true },
                    saveAsImage: { show: true }
                }
            },
            calculable: true,
            xAxis: [
                {
                    type: 'category',
                    boundaryGap: false,
                    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    name: '邮件营销',
                    type: 'line',
                    stack: '总量',
                    symbol: 'none',
                    itemStyle: {
                        normal: {
                            areaStyle: {
                                // 区域图，纵向渐变填充
                                color: 'orange'
                                // color: (function () {
                                //     var zrColor = require('zrender/tool/color');
                                //     return zrColor.getLinearGradient(
                                //         0, 200, 0, 400,
                                //         [[0, 'rgba(255,0,0,0.8)'], [0.8, 'rgba(255,255,255,0.1)']]
                                //     )
                                // })()
                            }
                        }
                    },
                    data: [
                        120, 132, 301, 134,
                        { value: 90, symbol: 'droplet', symbolSize: 5 },
                        230, 210
                    ]
                },
                {
                    name: '联盟广告',
                    type: 'line',
                    stack: '总量',
                    smooth: true,
                    symbol: 'image://../asset/ico/favicon.png',     // 系列级个性化拐点图形
                    symbolSize: 8,
                    data: [
                        120, 82,
                        {
                            value: 201,
                            symbol: 'star',  // 数据级个性化拐点图形
                            symbolSize: 15,
                            itemStyle: {
                                normal: {
                                    label: {
                                        show: true,
                                        textStyle: {
                                            fontSize: '20',
                                            fontFamily: '微软雅黑',
                                            fontWeight: 'bold'
                                        }
                                    }
                                }
                            }
                        },
                        {
                            value: 134,
                            symbol: 'none'
                        },
                        190,
                        {
                            value: 230,
                            symbol: 'emptypin',
                            symbolSize: 8
                        },
                        110
                    ]
                },
                {
                    name: '直接访问',
                    type: 'line',
                    stack: '总量',
                    symbol: 'arrow',
                    symbolSize: 6,
                    symbolRotate: -45,
                    itemStyle: {
                        normal: {
                            color: 'red',
                            lineStyle: {        // 系列级个性化折线样式
                                width: 2,
                                type: 'dashed'
                            }
                        },
                        emphasis: {
                            color: 'blue'
                        }
                    },
                    data: [
                        320, 332, '-', 334,
                        {
                            value: 390,
                            symbol: 'star6',
                            symbolSize: 20,
                            symbolRotate: 10,
                            itemStyle: {        // 数据级个性化折线样式
                                normal: {
                                    color: 'yellowgreen'
                                },
                                emphasis: {
                                    color: 'orange',
                                    label: {
                                        show: true,
                                        position: 'inside',
                                        textStyle: {
                                            fontSize: '20'
                                        }
                                    }
                                }
                            }
                        },
                        330, 320
                    ]
                },
                {
                    name: '搜索引擎',
                    type: 'line',
                    symbol: 'emptyCircle',
                    itemStyle: {
                        normal: {
                            lineStyle: {            // 系列级个性化折线样式，横向渐变描边
                                width: 2,
                                color: 'orange',
                                // color: (function () {
                                //     var zrColor = require('zrender/tool/color');
                                //     return zrColor.getLinearGradient(
                                //         0, 0, 1000, 0,
                                //         [[0, 'rgba(255,0,0,0.8)'], [0.8, 'rgba(255,255,0,0.8)']]
                                //     )
                                // })(),
                                shadowColor: 'rgba(0,0,0,0.5)',
                                shadowBlur: 10,
                                shadowOffsetX: 8,
                                shadowOffsetY: 8
                            }
                        },
                        emphasis: {
                            label: { show: true }
                        }
                    },
                    data: [
                        620, 732, 791,
                        { value: 734, symbol: 'emptyHeart', symbolSize: 10 },
                        890, 930, 820
                    ]
                }
            ]
        };



        // 绘制图表
        myChart.setOption(option);
    }
    render() {
        return (
            <div id="main" style={{ width: 400, height: 400 }}></div>
        );
    }
}

export default EchartsTest;