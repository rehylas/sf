import React from "react";
import {
  G2,
  Chart,
  Geom,
  Axis,
  Tooltip,
  Coord,
  Label,
  Legend,
  View,
  Guide,
  Shape,
  Facet,
  Util
} from "bizcharts";
import DataSet from "@antv/data-set";
import request from '../utils/request'


class Mychart extends React.Component { //bizcharts  Chart 试验

    constructor(props) {
        super(props);
        this.state = {  };
    }
  
    componentDidMount() {
        console.log( "Mychart DidMount " )
 
    }

    render() {
        console.log( 'Mychart render '  )
        let data =[{'xval':'20181101','yval':'10','yval2':'30'},
                    {'xval':'20181102','yval':'20.0','yval2':'30'},
                    {'xval':'20181109','yval':'30.1','yval2':'30' } ]

        // const scale = {
        //     'sales': {
        //         type: 'identity' | 'linear' | 'cat' | 'time' | 'timeCat' | 'log' | 'pow', // 指定数据类型
        //         alias: string, // 数据字段的别名
        //         formatter: () => {}, // 格式化文本内容
        //         range: array, // 输出数据的范围，默认[0, 1]，格式为 [min, max]，min 和 max 均为 0 至 1 范围的数据。
        //         tickCount: number, // 设置坐标轴上刻度点的个数
        //         ticks: array, // 用于指定坐标轴上刻度点的文本信息，当用户设置了 ticks 就会按照 ticks 的个数和文本来显示
        //         sync: boolean // 当 chart 存在不同数据源的 view 时，用于统一相同数据属性的值域范围
        //     }
        //     };       
        
        const scale = {
            sales:{
              type:"linear",
              tickInterval:100,
            },
          }

        return (
            <div>
                <Chart   width={600} height={400} data={data}>
                
                <Legend name='xval'/>
                <Axis name="yval" />
                <Axis name="xval" /> 
                {/* geom type  = line,  interval */}
                <Geom type="line" position="xval*yval" color="ffffff"  >  <Label content="yval" />   </Geom>
                <Geom type="point" position="xval*yval2" color="red" />
                <Tooltip crosshairs={{
                    //rect: 矩形框,x: 水平辅助线,y: 垂直辅助线,cross: 十字辅助线。 || 'x' || 'y' || 'cross',
                    type: 'rect' ,
                    offset:1,
                    
                    style: {
                        lineWidth:2,
                        
                        stroke:"#ff0000",
                    }
                }}/>

                </Chart>
            </div>    
        )        
    }

}


export default Mychart;


